import os
import re
from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
    
class ColorSort:
    @staticmethod
    def isin_refcolors(color_string, reference_colors_lower: set[str]) -> bool:
        words = re.split(r'[,&]', color_string)
        words = [word.strip() for word in words if word.strip()]
        words = [word.lower() for word in words]
        # print(words)
        
        if len(words) > 2:
            return all(word in reference_colors_lower for word in words[:2])
        return all(word in reference_colors_lower for word in words) 
    
    @staticmethod
    def assign_f2_colors(color_string: str) -> str|None:
        if not isinstance(color_string, str):  # Handle non-string cases
            return None  

        words = re.split(r'[,&]', color_string)
        words = [word.strip().lower() for word in words if word.strip()]
        
        # Select matched colors (first 2 if more than 2, all otherwise)
        matched_colors = [word for word in (words[:2] if len(words) > 2 else words)]
        
        return ", ".join(matched_colors) if matched_colors else None
    
    @staticmethod
    def get_diff_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        return df1.merge(df2, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

    @staticmethod
    def group_by_f2_colors(df2: pd.DataFrame, GROUP_FOLDER_PATH: str) -> None:
        grouped_data = df2.groupby('f2_colors')
        grouped_dfs = {}
        for color, group in grouped_data:
            grouped_dfs[color] = group.reset_index(drop=True)

        print(f"Number of unique colors: {len(grouped_dfs.keys())}")
        print(f"Number of total rows: {len(df2)}")

        for color, df in grouped_dfs.items():
            # Replace spaces and special characters in the color string with underscores
            filename = f"{color.replace(' ', '_').replace('&', 'and').replace(',', '').replace('/', '_')}_{len(df)}.csv"
            # Save the DataFrame to a CSV file
            df.to_csv(f"{GROUP_FOLDER_PATH}/{filename}", index=False)
        
        print(f"Grouped CSV files saved to {GROUP_FOLDER_PATH}")
    
    @staticmethod
    def read_group_data(file_path: str) -> pd.DataFrame:
        file_data = []

        for filename in os.listdir(file_path):
            if filename.endswith(".csv"):
                # Remove `.csv` and split at the last underscore
                name = filename[:-4]
                *color_parts, count = name.split('_')
                color = '_'.join(color_parts)
                file_data.append((color.replace('_', ' '), int(count)))

        grouped_df = pd.DataFrame(file_data, columns=["color_combo", "count"])
        
        return grouped_df
    
    @staticmethod
    def get_color_combos(grouped_df: pd.DataFrame, threshold: int = 10) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df_sorted = grouped_df.sort_values("count", ascending=False).reset_index(drop=True)
        df_above = df_sorted[df_sorted["count"] >= threshold]
        df_below = df_sorted[df_sorted["count"] < threshold]

        # Combine the 'Others'
        other_total = df_below["count"].sum()
        df_final = df_above.copy()
        df_final.loc[len(df_final)] = ["Other", other_total]
        
        return df_final, df_below
    
    @staticmethod
    def plot_color_combos(df_final: pd.DataFrame, df_below: pd.DataFrame) -> None:
        plt.figure(figsize=(12, 6))
        bars = plt.bar(df_final["color_combo"], df_final["count"], color="skyblue")
        plt.xticks(rotation=45, ha='right')
        plt.title("Color Combinations by Row Count")
        plt.ylabel("Row Count")
        plt.tight_layout()

        # Annotate the 'Other' bar
        if "Other" in df_final["color_combo"].values:
            idx = df_final[df_final["color_combo"] == "Other"].index[0]
            combos = ", ".join(df_below["color_combo"].tolist())
            bars[idx].set_color("lightcoral")
            plt.text(idx, df_final["count"].iloc[idx] + 1, f"{len(df_below)} combos", ha='center', va='bottom', fontsize=8)
