import csv
import requests
import json
import re
import os
import time
#
# Cấu trúc của các khu vực và universe cần collect
regions_config = [
    #{"region": "USA", "universe": "TOP3000", "folder": "USA_data"},
    {"region": "GLB", "universe": "MINVOL1M", "folder": "GLB_data"},
    #{"region": "EUR", "universe": "TOP2500", "folder": "EUR_data"},
    #{"region": "ASI", "universe": "MINVOL1M", "folder": "ASI_data"},
]

# Cấu hình chung
alpha_count = 50  # chỉnh giới hạn alpha use, để trống nếu không cần
user_count = 20   # chỉnh giới hạn user use, để trống nếu không cần
number_of_page = 40  # chỉnh số trang muốn lấy
limit_per_page = 20  # chỉnh số field collect mỗi trang

# Thư mục gốc để lưu tất cả dữ liệu
base_output_dir = "worldquant_data_regions"

def ensure_directory_exists(directory_path):
    """Đảm bảo thư mục tồn tại, nếu không thì tạo mới"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def start_session():
    global headers, cookie

    try:
        with open(r'C:\Users\Administrator\Desktop\alpha\cookie.txt') as file:
            cookie = file.read().strip()  # Remove trailing newline if any

        if cookie:
            s = requests.Session()
            headers = {'Cookie': cookie,
                       'Host': 'api.worldquantbrain.com',
                       'Connection': 'keep-alive'}
            print('Logged in')
            s.headers.update(headers)
            return s
        else:
            print("No cookie found. Please ensure you have logged in and saved the cookie.")
            return None
    except Exception as e:
        print(f"Failed to start session: {e}")
        return None
    
def write_txt(filepath, data):
    # Đảm bảo thư mục tồn tại
    directory = os.path.dirname(filepath)
    ensure_directory_exists(directory)
    
    # Ghi dữ liệu vào file
    with open(filepath, 'w', encoding='utf-8') as txtfile:
        for item in data:
            txtfile.write(f"{item}\n")

def get_data_api(s, full_url):
    data = None
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = s.get(full_url)
            if "Retry-After" in response.headers:
                retry_after = float(response.headers["Retry-After"])
                print(f"Rate limited. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            else:
                response.raise_for_status()
                data = response.json().get('results', [])
                print(f"Got {len(data)} items")
                break
        except requests.exceptions.RequestException as e:
            retry_count += 1
            print(f"Request failed ({retry_count}/{max_retries}): {e}")
            time.sleep(5)
            
    return data or []

def filter_data(data):
    data_valid = []
    for item in data:
        if alpha_count is not None and user_count is not None:
            if item.get('alphaCount', 0) >= alpha_count and item.get('userCount', 0) >= user_count:
                data_valid.append(item)
        elif alpha_count is not None:
            if item.get('alphaCount', 0) >= alpha_count:
                data_valid.append(item)
        elif user_count is not None:
            if item.get('userCount', 0) >= user_count:
                data_valid.append(item)
        else:
            data_valid.append(item)  # Nếu không có bộ lọc, lấy tất cả
    return data_valid

def process_region_data(s, region_config):
    base_url = "https://api.worldquantbrain.com/data-fields?"
    params = {
        "delay": 1,
        "instrumentType": "EQUITY",
        "limit": limit_per_page,
        "offset": 0,
        "order": "-alphaCount",
        "region": region_config["region"],
        "universe": region_config["universe"],
        "type": ""  # để trống để collect tất cả type
    }
    
    region_name = region_config["region"]
    region_folder = region_config["folder"]
    
    # Tạo đường dẫn đầy đủ đến thư mục output cho region này
    region_output_dir = os.path.join(base_output_dir, region_folder)
    ensure_directory_exists(region_output_dir)
    
    print(f"\n--- Collecting data for {region_name} region with {region_config['universe']} universe ---")
    
    # Initialize empty lists
    data_raw = []
    data_matrix = []
    data_vector = []
    data_group = []
    data_universe = []
    data_Opvec_and_matrix = []
    
    # Collect data from all pages
    for i in range(1, number_of_page + 1):
        params["offset"] = (i - 1) * params["limit"]
        full_url = requests.Request('GET', base_url, params=params).prepare().url
        print(f"Requesting page {i} for {region_name}...")
        page_data = get_data_api(s, full_url)
        if not page_data:
            print(f"No more data for {region_name} at page {i}")
            break
        data_raw.extend(page_data)
    
    # Filter data
    data_valid = filter_data(data_raw)
    print(f"Found {len(data_valid)} valid items for {region_name}")
    
    # Process data by type
    for item in data_valid:
        item_type = item.get('type')
        item_id = item.get('id')
        
        if not item_id:
            continue
            
        if item_type == "MATRIX":
            data_matrix.append(item_id)
            data_Opvec_and_matrix.append(item_id)
        elif item_type == "VECTOR":
            data_vector.append(item_id)
            data_Opvec_and_matrix.append(f"vec_avg({item_id})")
        elif item_type == "GROUP":
            data_group.append(item_id)
        elif item_type == "UNIVERSE":
            data_universe.append(item_id)
    
    # Save data to files in the region output directory
    write_txt(os.path.join(region_output_dir, "All_Matrix_And_OP(Vector).txt"), data_Opvec_and_matrix)
    write_txt(os.path.join(region_output_dir, "Matrix.txt"), data_matrix)
    write_txt(os.path.join(region_output_dir, "Vector.txt"), data_vector)
    write_txt(os.path.join(region_output_dir, "Group.txt"), data_group)
    write_txt(os.path.join(region_output_dir, "Universe.txt"), data_universe)
    
    print(f"Saved data files for {region_name} in {region_output_dir}")
    
    return {
        "region": region_name,
        "total_items": len(data_valid),
        "matrix_count": len(data_matrix),
        "vector_count": len(data_vector),
        "group_count": len(data_group),
        "universe_count": len(data_universe)
    }

def main():
    # Đảm bảo thư mục gốc tồn tại
    ensure_directory_exists(base_output_dir)
    
    # Khởi tạo session
    s = start_session()
    if not s:
        print("Failed to start session. Exiting...")
        return
    
    results = []
    
    # Process each region configuration
    for region_config in regions_config:
        result = process_region_data(s, region_config)
        results.append(result)
    
    # Print summary
    print("\n--- Collection Summary ---")
    for result in results:
        print(f"Region: {result['region']}")
        print(f"  Total items: {result['total_items']}")
        print(f"  Matrix: {result['matrix_count']}")
        print(f"  Vector: {result['vector_count']}")
        print(f"  Group: {result['group_count']}")
        print(f"  Universe: {result['universe_count']}")
        print("----------------------------")
    
    # Ghi file tổng kết
    summary_path = os.path.join(base_output_dir, "collection_summary.txt")
    with open(summary_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write("--- Collection Summary ---\n")
        for result in results:
            summary_file.write(f"Region: {result['region']}\n")
            summary_file.write(f"  Total items: {result['total_items']}\n")
            summary_file.write(f"  Matrix: {result['matrix_count']}\n")
            summary_file.write(f"  Vector: {result['vector_count']}\n")
            summary_file.write(f"  Group: {result['group_count']}\n")
            summary_file.write(f"  Universe: {result['universe_count']}\n")
            summary_file.write("----------------------------\n")
    
    print(f"Collection summary saved to {summary_path}")
    print("Data collection completed!")

if __name__ == "__main__":
    main()