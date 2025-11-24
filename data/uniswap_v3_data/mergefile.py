import pandas as pd
import glob


def merge_csv_files(pattern, output_file="merged_data.csv"):
    """合并多个CSV文件"""
    csv_files = glob.glob(pattern)
    dfs = []

    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)
        print(f"已读取: {file} ({len(df)} 行)")

    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_csv(output_file, index=False)
    print(f"合并完成: {output_file} ({len(merged_df)} 行)")

    return merged_df

# 使用示例
merge_csv_files("uniswap_data*.csv", "combined_uniswap_data.csv")