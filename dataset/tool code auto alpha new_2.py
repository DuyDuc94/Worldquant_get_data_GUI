import itertools
#
# Đọc dữ liệu từ file
with open("data_input.txt", "r") as my_file:
    alphas = [line.strip() for line in my_file if line.strip()]

print(f"Tìm thấy {len(alphas)} alpha trong file data_input.txt")

# Kiểm tra số lượng alpha
if len(alphas) < 2:
    print("Không đủ alpha.")
else:
    with open("alpha.txt", "w") as output_file:
        count = 0
        
        # Tạo tổ hợp 2 phần tử từ danh sách alpha
        for combination in itertools.combinations(alphas, 2):
            scaled_alphas = [f"scale({alpha})" for alpha in combination]
            
            expressions = [
                f"add({','.join(scaled_alphas)}, filter=True)",
                #f"multiply({','.join(scaled_alphas)}, filter=True)",
                #f"subtract({','.join(scaled_alphas)}, filter=True)",
                #f"divide({','.join(scaled_alphas)}, filter=True)"
            ]
            
            for expr in expressions:
                output_file.write(expr + "\n")
                count += 1

    print(f"Đã tạo {count} biểu thức")

    # Tính toán lý thuyết
    n = len(alphas)
    combinations_2 = n * (n - 1) // 2  # C(n,2)
    total_theoretical = combinations_2 * 4  # Nhân 4 vì có 4 phép toán

    print(f"Số lượng tối đa lý thuyết: {total_theoretical:,} biểu thức")
    print(f"Tổ hợp 2 phần tử: C({n},2) = {combinations_2:,}")
    print(f"Mỗi tổ hợp tạo 4 biểu thức (add, multiply, subtract, divide)")
