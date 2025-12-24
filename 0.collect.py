import requests
import json
import pandas as pd
import datetime
import pytz
import time
import urllib.parse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===========================================
# Query Configuration
# ===========================================

# Base URL for fetching alphas

base_url = "https://api.worldquantbrain.com/users/self/alphas"

# Construct the params dictionary with activated parameters
params = {
    # Pagination Parameters
    "limit": 100,
    "offset": 0,

    # Alpha Type and Status
     "status": "UNSUBMITTED\x1FIS_FAIL",
    #"status": "ACTIVE\x1FIS_FAIL",
    "type": "REGULAR",
    # # Date Filters   yyyy-mm-dd
    #"dateSubmitted>": "2024-10-01T00:00:00-04:00",
    "dateCreated>": "2025-11-15T00:00:00-04:00",
    # # "dateCreated<": "2024-11-08T00:00:00-04:00",
#
    # # Settings Parameters
    "settings.region": "GLB",
    "settings.universe": "MINVOL1M",              # Universe (e.g., TOP3000, MINVOL1M)
    #"settings.decay": 8,                # Decay value
    # # "settings.delay": 0,                         # Delay value
    # # "settings.neutralization": "CROWDING",    # Neutralization (e.g., SUBINDUSTRY)
    #"settings.truncation": 0.07,                 # Truncation value
    # # "settings.pasteurization": "ON",             # Pasteurization (ON or OFF)
    # # "settings.nanHandling": "ON",                # NaN Handling (ON or OFF)

    # # # # Performance Metrics - In-Sample (IS)
    "is.sharpe>": 3,
    #"is.sharpe<": 5,

    "is.fitness>": 2,
    "is.longCount>":100,
    "is.shortCount>": 100,
    #"is.sharpe<": -1.4,
    #"is.fitness<": -0.9,   
    # # # # "is.drawdown<": 0.1,         # IS Drawdown less than 10%
    # # # "is.turnover<": 0.3,         # IS Turnover less than 0.5
    # # # "is.margin>": 0.0005,        # IS Margin greater than 0.0005
    # "is.pnl>": 2000000,          # IS PnL greater than 1,000,000
    #
    # # # Sorting and Ordering
    # # "order": "-is.fitness",

    # Visibility
    # "hidden": "false",
    
    # Investability Constrained Filters at API level
    # "is.investabilityConstrained.sharpe>": 1.4,
    # "is.investabilityConstrained.fitness>": 0.9,
}

# ===========================================
# Filter Conditions
# ===========================================

filter_conditions = {
    # ===========================
    # General Alpha Settings
    # ===========================
    # 'Region': '== "ASI"',                     # Filter alphas by region (e.g., "GLB", "USA", "JPN")
    # 'Instrument Type': '== "EQUITY"',         # Filter by instrument type (e.g., "EQUITY", "FUTURE")
    # 'Universe': '== "TOP3000"',               # Filter by universe (e.g., "TOP3000", "MINVOL1M")
    # 'Delay': '== 1',                          # Filter by delay value
    # 'Decay': '== 1',                          # Filter by decay value
    # 'Neutralization': '== "SUBINDUSTRY"',     # Filter by neutralization method
    # 'Truncation': '<= 0.05',                  # Filter by truncation value
    # 'Pasteurization': '== "ON"',              # Filter by pasteurization setting ("ON" or "OFF")
    # 'Unit Handling': '== "VERIFY"',           # Filter by unit handling method ("VERIFY", "ADJUST", "OFF")
    # 'NaN Handling': '== "ON"',                # Filter by NaN handling setting ("ON" or "OFF")
    # 'Language': '== "FASTEXPR"',              # Filter by language used ("FASTEXPR", "PYTHON")
    # 'Visualization': '== False',              # Filter alphas with or without visualization

    # ===========================
    # Author and Status
    # ===========================
    # 'Author': '== "YourUsername"',            # Filter by author username
    # 'Stage': '== "IS"',                       # Filter by stage ("IS", "OS")
    # 'Status': '== "UNSUBMITTED"',             # Filter by status ("UNSUBMITTED", "ACTIVE", etc.)
    # 'Favorite': '== True',                    # Filter alphas marked as favorite (True or False)
    # 'Hidden': '== False',                     # Filter alphas that are not hidden (True or False)

    # ===========================
    # Performance Metrics - In-Sample (IS)
    # ===========================
    # 'IS PnL': '> 1000000',                    # IS PnL greater than a value
    # 'IS Sharpe': '> 1.5',                     # IS Sharpe Ratio greater than a value
    # 'IS Fitness': '> 1.0',                    # IS Fitness greater than a value
    # 'IS Turnover': '< 0.5',                   # IS Turnover less than a value
    # 'IS Returns': '> 0.05',                   # IS Returns greater than a value
    # 'IS Drawdown': '<= 0.1',                  # IS Drawdown less than or equal to a value
    # 'IS Margin': '> 0.0005',                  # IS Margin greater than a value
    # 'Long Count': '>= 500',                   # IS Long Count greater than or equal to a value
    # 'Short Count': '>= 500',                  # IS Short Count greater than or equal to a value
    # 'Book Size': '> 10000000',                # IS Book Size greater than a value

    # ===========================
    # Performance Metrics - Out-of-Sample (OS)
    # ===========================
    # 'OS PnL': '> 500000',                     # OS PnL greater than a value
    # 'OS Sharpe': '> 1.3',                     # OS Sharpe Ratio greater than a value
    # 'OS Fitness': '> 0.9',                    # OS Fitness greater than a value
    # 'OS Returns': '> 0.04',                   # OS Returns greater than a value
    # 'OS Turnover': '< 0.3',                   # OS Turnover less than a value
    # 'OS Drawdown': '< 0.1',                   # OS Drawdown less than a value
    # 'OS Margin': '> 0.0005',                  # OS Margin greater than a value

    # ===========================
    # Checks and Classifications
    # ===========================
    # Use 'Value' or 'Result' to specify which aspect you're filtering on.
    # For example, to filter alphas where the 'LOW_SHARPE' check resulted in 'FAIL':
    # 'LOW_SHARPE Result': '== "FAIL"'
    # Or to filter alphas where the 'LOW_2Y_SHARPE' check value is greater than 1.6:
    # 'LOW_2Y_SHARPE Value': '> 1.6'
    # # ===========================
    # # #SETTING FOR UNSUBMITTED ALPHA
    # # # # ===========================
    # # # # 'Classification ID': '.str.contains("DATA_USAGE:SINGLE_DATA_SET")',   # Filter by classification ID
     #'LOW_SHARPE Result': '== "PASS"',             # Filter alphas that failed the LOW_SHARPE check
     #'LOW_FITNESS Result': '== "PASS"',            # Filter alphas that failed the LOW_FITNESS check
     #'LOW_TURNOVER Result': '== "PASS"',           # Filter alphas that passed the LOW_TURNOVER check
     #'HIGH_TURNOVER Result': '== "PASS"',          # Filter alphas that passed the HIGH_TURNOVER check
     'LOW_SUB_UNIVERSE_SHARPE Result': '== "PASS"',    # Filter alphas with LOW_SUB_UNIVERSE_SHARPE value greater than 0.6
     'LOW_ROBUST_UNIVERSE_SHARPE Result': '== "PASS"',    # Filter alphas with LOW_SUB_UNIVERSE_SHARPE value greater than 0.6
     'LOW_ROBUST_UNIVERSE_RETURNS Result': '== "PASS"',    # Filter alphas with LOW_SUB_UNIVERSE_SHARPE value greater than 0.6

     #'LOW_SUB_UNIVERSE_SHARPE Value': '> 2',     # Filter alphas with LOW_SUB_UNIVERSE_SHARPE value greater than 0.6
    # # 'SELF_CORRELATION Result': '== "PENDING"',    # Filter alphas with SELF_CORRELATION check pending
    # # 'DATA_DIVERSITY Result': '== "PENDING"',      # Filter alphas with DATA_DIVERSITY check pending
    # # 'PROD_CORRELATION Result': '== "PENDING"',    # Filter alphas with PROD_CORRELATION check pending
     #'REGULAR_SUBMISSION Result': '== "PENDING"',  # Filter alphas with REGULAR_SUBMISSION check pending
    # # # 'MATCHES_COMPETITION Result': '== "PASS"',    # Filter alphas that passed the MATCHES_COMPETITION check
    'CONCENTRATED_WEIGHT Result': '== "PASS"',    # Filter alphas that passed the CONCENTRATED_WEIGHT check
    'LOW_GLB_AMER_SHARPE Result': '== "PASS"',    # Phải pass check
   # 'LOW_GLB_AMER_SHARPE Value': '> 1.58',        # Sharpe ratio > 1.58

# 2. EMEA (Châu Âu, Trung Đông, Châu Phi) - Sharpe > 1.58  
    'LOW_GLB_EMEA_SHARPE Result': '== "PASS"',    # Phải pass check
    #'LOW_GLB_EMEA_SHARPE Value': '> 1.58',        # Sharpe ratio > 1.58

# 3. APAC (Châu Á Thái Bình Dương) - Sharpe > 1.58
    'LOW_GLB_APAC_SHARPE Result': '== "PASS"',    # Phải pass check  
    #'LOW_GLB_APAC_SHARPE Value': '> 1.58',        # Sharpe ratio > 1.58
    # 'IS_LADDER_SHARPE Result': '== "PASS"',
    #'LOW_2Y_SHARPE Value': '> 1.7',               # Filter alphas with LOW_2Y_SHARPE value greater than 1.6
    # # 'MATCHES_THEMES Result': '== "PASS"',         # Filter alphas that passed the MATCHES_THEMES check

    # ===========================
    # Investability Constrained Filters
    # ===========================
    #'IC Sharpe': '> 1.6',                # Filter by Investability Constrained Sharpe
    #'IC Fitness': '> 0.8',               # Filter by Investability Constrained Fitness
    # 'IC Turnover': '< 0.1',            # Filter by Investability Constrained Turnover
    # 'IC Returns': '> 0.04',            # Filter by Investability Constrained Returns
    # 'IC Drawdown': '< 0.1',            # Filter by Investability Constrained Drawdown
    # 'IC Margin': '> 0.0005',           # Filter by Investability Constrained Margin
    # 'IC Long Count': '> 300',          # Filter by Investability Constrained Long Count
    # 'IC Short Count': '> 300',         # Filter by Investability Constrained Short Count
    # 'IC PnL': '> 5000000',             # Filter by Investability Constrained PnL

    # ===========================
    # Date Filters
    # ===========================
    # 'Date Created': '>= "2024-01-01"',        # Alphas created on or after this date
    # 'Date Created': '<= "2024-12-31"',        # Alphas created on or before this date
    # 'Date Modified': '>= "2024-01-01"',       # Alphas modified on or after this date
    # 'Date Modified': '<= "2024-12-31"',       # Alphas modified on or before this date
    # 'Date Submitted': '>= "2024-01-01"',      # Alphas submitted on or after this date
    # 'Date Submitted': '<= "2024-12-31"',      # Alphas submitted on or before this date

    # ===========================
    # Custom Conditions
    # ===========================
    # 'Operator Count': '<= 20',                # Alphas with operator count less than or equal to 20
    # 'Code': '.str.contains("vec_ir")',        # Alphas whose code contains "vec_ir"
    # 'Name': '.str.contains("my_alpha")',      # Alphas whose name contains "my_alpha"
    # 'Tags': '.str.contains("momentum")',      # Alphas tagged with "momentum"
    # 'Competition': '.str.contains("comp_id")',# Alphas participating in a specific competition
    # 'Classification ID': '.str.contains("your_classification")',  # Filter by custom classification
}


# ===========================================
# Rest of the Code
# ===========================================

# Function to construct the API URL with query parameters
def construct_url(base_url, params):
    def encode_param_key(k):
        # Split the key into name and operator
        match = re.match(r'([a-zA-Z0-9_.]+)([><])?', k)
        if match:
            name = match.group(1)
            operator = match.group(2) or ''
            name_encoded = urllib.parse.quote_plus(name)
            operator_encoded = urllib.parse.quote_plus(operator)
            return name_encoded + operator_encoded
        else:
            return urllib.parse.quote_plus(k)

    def encode_value(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%dT%H:%M:%S%z')
        return str(value)

    query_string = '&'.join(
        [f"{encode_param_key(k)}={urllib.parse.quote_plus(encode_value(v))}" for k, v in params.items()])
    full_url = f"{base_url}?{query_string}"
    return full_url

# Function to fetch alpha data with retries
def fetch_alpha_data(session, url, offset):
    retries = 5
    for i in range(retries):
        try:
            response = session.get(url + f"&offset={offset}", headers=session.headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and "results" in data:
                return data
            else:
                print(f"Unexpected response format for offset {offset}: {data}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Request failed for offset {offset}: {e}")
            if i < retries - 1:
                sleep_time = 2 ** i  # Exponential backoff
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Failed after {retries} attempts for offset {offset}.")
                return {}

# Function to apply conditional filters for IS_LADDER_SHARPE and LOW_2Y_SHARPE
# Function to apply conditional filters for IS_LADDER_SHARPE and LOW_2Y_SHARPE

def apply_conditional_filters(df):
    """
    Apply conditional filter: check IS_LADDER_SHARPE Value > 1.7 if present,
    otherwise allow LOW_2Y_SHARPE Value > 1.7. Logs number of dropped alphas.
    """
    print(f"Before conditional filtering: {len(df)} alphas")

    # Check if columns exist
    if 'IS_LADDER_SHARPE Value' not in df.columns and 'LOW_2Y_SHARPE Value' not in df.columns:
        print("Neither IS_LADDER_SHARPE Value nor LOW_2Y_SHARPE Value columns found. Skipping conditional filter.")
        return df

    # Check for non-null IS_LADDER_SHARPE Value and apply threshold
    if 'IS_LADDER_SHARPE Value' in df.columns:
        has_ladder_sharpe = df['IS_LADDER_SHARPE Value'].notna()
        ladder_sharpe_high = df['IS_LADDER_SHARPE Value'] > 1.6
    else:
        has_ladder_sharpe = pd.Series([False] * len(df))
        ladder_sharpe_high = pd.Series([False] * len(df))

    # Check for non-null and high LOW_2Y_SHARPE Value
    if 'LOW_2Y_SHARPE Value' in df.columns:
        high_2y_sharpe = df['LOW_2Y_SHARPE Value'] > 1.6
    else:
        high_2y_sharpe = pd.Series([False] * len(df))

    # Combined mask for keeping
    keep_mask = (has_ladder_sharpe & ladder_sharpe_high) | (~has_ladder_sharpe & high_2y_sharpe)

    # If no valid conditions, keep all
    if not keep_mask.any():
        print("No alphas meet the conditional filter criteria. Keeping all alphas.")
        return df

    # Breakdown of dropped alphas
    total_dropped = (~keep_mask).sum()
    dropped_by_ladder = (has_ladder_sharpe & ~ladder_sharpe_high).sum()
    dropped_by_2y_sharpe = (~has_ladder_sharpe & ~high_2y_sharpe).sum()

    print(f"Alphas dropped by conditional filter: {total_dropped}")
    print(f"  → Dropped due to IS_LADDER_SHARPE <= 1.7: {dropped_by_ladder}")
    print(f"  → Dropped due to LOW_2Y_SHARPE <= 1.7 (when IS_LADDER_SHARPE missing): {dropped_by_2y_sharpe}")

    filtered_df = df[keep_mask]

    print(f"After conditional filtering: {len(filtered_df)} alphas")
    return filtered_df


# Main function to collect, process, and filter alpha data
def collect_and_process_alpha_data(session, url, output_file, num_alphas, filter_conditions):
    start_time = datetime.datetime.now()
    print('Collecting alpha data...', start_time.strftime("%Y-%m-%d %H:%M:%S"))

    # Initialize list to store alphas
    all_alphas = []

    # Get the total number of alphas to collect
    response = session.get(url, headers=session.headers)
    data = response.json()
    if not isinstance(data, dict):
        print(f"Unexpected response format: {data}")
        return

    num_alphas_to_collect = data.get("count", 0)
    print("Number of alphas to collect:", num_alphas_to_collect)

    offset = 0
    limit = 100

    offsets = [offset + i * limit for i in range((num_alphas_to_collect + limit - 1) // limit)]
    print("Offsets:", offsets)

    # Progress tracking variables
    total_offsets = len(offsets)
    alphas_collected = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_offset = {executor.submit(fetch_alpha_data, session, url, offset): offset for offset in offsets}

        for future in as_completed(future_to_offset):
            current_offset = future_to_offset[future]
            try:
                data = future.result()
                if "results" not in data:
                    continue

                all_alphas.extend(data["results"])
                alphas_collected += len(data["results"])

                # Print progress
                print(f"Progress: Collected {alphas_collected}/{num_alphas_to_collect} alphas.")

                # If you want to limit the number of alphas collected
                if num_alphas > 0 and len(all_alphas) >= num_alphas:
                    all_alphas = all_alphas[:num_alphas]
                    break
            except Exception as e:
                print(f'Exception fetching data for offset {current_offset}:', e)
                continue

    print(f"Total alphas collected: {len(all_alphas)}")

    # Process the collected alphas into a DataFrame
    alpha_list = []
    for idx, alpha in enumerate(all_alphas, start=1):
        # Debugging để xem cấu trúc dữ liệu alpha
        if idx == 1:
            print("Sample alpha structure:")
            if 'is' in alpha and 'investabilityConstrained' in alpha['is']:
                print("Found investabilityConstrained in the data structure")
            else:
                print("WARNING: investabilityConstrained not found in the data structure")
                if 'is' in alpha:
                    print("Keys in 'is':", alpha['is'].keys())
        
        # Lấy metrics
        is_metrics = alpha.get('is', {})
        os_metrics = alpha.get('os', {}) if alpha.get('os') else {}
        
        # Lấy dữ liệu Investability Constrained
        ic_metrics = is_metrics.get('investabilityConstrained', {})
        
        checks = is_metrics.get('checks', []) + os_metrics.get('checks', [])

        # Separate 'value' and 'result' for each check
        check_values = {}
        for check in checks:
            name = check.get('name')
            value = check.get('value')
            result = check.get('result')
            check_values[f'{name} Value'] = value
            check_values[f'{name} Result'] = result

        classifications = alpha.get('classifications', [])
        classification_ids = ', '.join([classification.get('id') for classification in classifications])

        # Handle the 'competitions' field, assuming each item is a dictionary
        competitions = alpha.get('competitions', [])
        if isinstance(competitions, list):
            # Join competition names or IDs, depending on what you need from each dictionary
            competition_str = ', '.join([comp.get('id', 'unknown') for comp in competitions])
        else:
            competition_str = ''

        # Process the 'Code' field to remove spaces and line breaks
        code = alpha['regular'].get('code', '')
        if code:
            code = code.replace(' ', '').replace('\n', '')
            code = code.strip()

        alpha_data = {
            'ID': alpha['id'],
            'Name': alpha.get('name'),
            'Type': alpha['type'],
            'Author': alpha['author'],
            'Instrument Type': alpha['settings'].get('instrumentType'),
            'Region': alpha['settings'].get('region'),
            'Universe': alpha['settings'].get('universe'),
            'Delay': alpha['settings'].get('delay'),
            'Decay': alpha['settings'].get('decay'),
            'Neutralization': alpha['settings'].get('neutralization'),
            'Truncation': alpha['settings'].get('truncation'),
            'Pasteurization': alpha['settings'].get('pasteurization'),
            'Unit Handling': alpha['settings'].get('unitHandling'),
            'NaN Handling': alpha['settings'].get('nanHandling'),
            'Language': alpha['settings'].get('language'),
            'Visualization': alpha['settings'].get('visualization'),
            'Code': code,
            'Operator Count': alpha['regular'].get('operatorCount'),
            'Date Created': alpha['dateCreated'],
            'Date Submitted': alpha['dateSubmitted'],
            'Date Modified': alpha['dateModified'],
            'Favorite': alpha['favorite'],
            'Hidden': alpha['hidden'],
            'Color': alpha['color'],
            'Category': alpha['category'],
            'Tags': ', '.join(alpha['tags']),
            'Stage': alpha['stage'],
            'Status': alpha['status'],
            'IS PnL': is_metrics.get('pnl'),
            'Book Size': is_metrics.get('bookSize'),
            'Long Count': is_metrics.get('longCount'),
            'Short Count': is_metrics.get('shortCount'),
            'IS Turnover': is_metrics.get('turnover'),
            'OS Turnover': os_metrics.get('turnover'),
            'IS Returns': is_metrics.get('returns'),
            'OS Returns': os_metrics.get('returns'),
            'IS Drawdown': is_metrics.get('drawdown'),
            'OS Drawdown': os_metrics.get('drawdown'),
            'IS Margin': is_metrics.get('margin'),
            'OS Margin': os_metrics.get('margin'),
            'IS Fitness': is_metrics.get('fitness'),
            'OS Fitness': os_metrics.get('fitness'),
            'IS Sharpe': is_metrics.get('sharpe'),
            'OS Sharpe': os_metrics.get('sharpe'),
            'Classification ID': classification_ids,
            'Competition': competition_str,
            
            # Thêm các trường Investability Constrained với tên đơn giản hơn
            'IC PnL': ic_metrics.get('pnl'),
            'IC Book Size': ic_metrics.get('bookSize'),
            'IC Long Count': ic_metrics.get('longCount'),
            'IC Short Count': ic_metrics.get('shortCount'),
            'IC Turnover': ic_metrics.get('turnover'),
            'IC Returns': ic_metrics.get('returns'),
            'IC Drawdown': ic_metrics.get('drawdown'),
            'IC Margin': ic_metrics.get('margin'),
            'IC Fitness': ic_metrics.get('fitness'),
            'IC Sharpe': ic_metrics.get('sharpe'),
        }
        alpha_data.update(check_values)
        alpha_list.append(alpha_data)

        # Print progress every 100 alphas processed
        if idx % 100 == 0 or idx == len(all_alphas):
            print(f"Processing alpha {idx}/{len(all_alphas)}")

    alpha_df = pd.DataFrame(alpha_list)

    # Thêm debug thông tin về dữ liệu sau khi xử lý
    print("Columns in DataFrame:", alpha_df.columns.tolist())
    if 'IC Sharpe' in alpha_df.columns:
        print("IC Sharpe statistics:")
        print(alpha_df['IC Sharpe'].describe())
    else:
        print("WARNING: IC Sharpe column not found in the processed data")

    # Apply filter conditions
    filtered_df = alpha_df.copy()
    for col, condition in filter_conditions.items():
        # Skip the IS_LADDER_SHARPE and LOW_2Y_SHARPE filters as we'll handle them specially
        if col in ['IS_LADDER_SHARPE Result', 'LOW_2Y_SHARPE Value']:
            continue
            
        try:
            if '.str.contains' in condition:
                # Handle string contains condition
                query_expr = f'{col}{condition}'
            else:
                query_expr = f'`{col}` {condition}'
            
            before_filter_count = len(filtered_df)
            filtered_df = filtered_df.query(query_expr, engine='python')
            after_filter_count = len(filtered_df)
            
            print(f"Filter '{col} {condition}' removed {before_filter_count - after_filter_count} alphas")
        except Exception as e:
            print(f"Error in filter condition for column '{col}': {e}")

    # Now apply our special conditional filter
    filtered_df = apply_conditional_filters(filtered_df)

    # Output filtered data to CSV
    filtered_df.to_csv(output_file, index=False)
    print("Filtered data has been saved to:", output_file)
    print(f"Total alphas after filtering: {len(filtered_df)}")

    end_time = datetime.datetime.now()
    print('Completed processing. Total time:', end_time - start_time)
#
def main():
    # Load cookie for authentication
    with open(r'C:\Users\Administrator\Desktop\alpha\cookie.txt') as file:
        cookie = file.read().strip()  # Remove trailing newline if any

    if cookie:
        session = requests.session()
        headers = {'Cookie': cookie, 'Host': 'api.worldquantbrain.com', 'Connection': 'keep-alive'}
        session.headers.update(headers)
    else:
        print("No cookie found. Please ensure you are logged in.")
        return

    print('Logged in')

    # Construct the full URL with parameters
    url = construct_url(base_url, params)
    print("Constructed URL:", url)

    output_file = '0.collected_alpha_data.csv'  # Output file name
    num_alphas_to_collect = 0  # Set to 0 to collect all

    # Collect, process, and filter the alpha data
    collect_and_process_alpha_data(session, url, output_file, num_alphas_to_collect, filter_conditions)

if __name__ == "__main__":
    main()