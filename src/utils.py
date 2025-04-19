import os
import re
from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
    
class ColorSort:
    """
    A utility class for handling and processing color-related data in various formats.
    Methods
    -------
    isin_refcolors(color_string, reference_colors_lower: set[str]) -> bool
        Checks if the colors in the given string are present in the reference set of colors.
    assign_f2_colors(color_string: str) -> str | None
        Assigns and formats the first two colors from the input string, if applicable.
    get_diff_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame
        Returns the rows that are present in the first DataFrame but not in the second.
    group_by_f2_colors(df2: pd.DataFrame, GROUP_FOLDER_PATH: str) -> None
        Groups a DataFrame by the 'f2_colors' column and saves each group as a CSV file.
    read_group_data(file_path: str) -> pd.DataFrame
        Reads grouped CSV files from a directory and returns a DataFrame summarizing the color combinations and their counts.
    get_color_combos(grouped_df: pd.DataFrame, threshold: int = 10) -> Tuple[pd.DataFrame, pd.DataFrame]
        Splits the grouped DataFrame into two: one above the threshold and one below, combining the below-threshold rows into an "Other" category.
    plot_color_combos(df_final: pd.DataFrame, df_below: pd.DataFrame) -> None
        Plots a bar chart of color combinations, highlighting the "Other" category if present.
    """
    
    @staticmethod
    def isin_refcolors(color_string, reference_colors_lower: set[str]) -> bool:
        """
        Checks if the words in a given color string are present in a set of reference colors.
        Args:
            color_string (str): A string containing color names separated by commas or ampersands.
            reference_colors_lower (set[str]): A set of reference color names in lowercase.
        Returns:
            bool: True if all words in the color string (up to the first two words if there are more than two)
                  are present in the reference colors set, otherwise False.
        Notes:
            - The function splits the input color string by commas and ampersands, trims whitespace,
              and converts the words to lowercase before checking against the reference set.
            - If the color string contains more than two words, only the first two are checked.
        """
        
        words = re.split(r'[,&]', color_string)
        words = [word.strip() for word in words if word.strip()]
        words = [word.lower() for word in words]
        # print(words)
        
        if len(words) > 2:
            return all(word in reference_colors_lower for word in words[:2])
        return all(word in reference_colors_lower for word in words) 
    
    @staticmethod
    def assign_f2_colors(color_string: str) -> str|None:
        """
        Extracts and returns up to the first two colors from a given color string.
        The function splits the input string by commas and ampersands, trims whitespace,
        and converts the words to lowercase. If the input is not a string, it returns None.
        If there are more than two colors, only the first two are returned. If there are
        two or fewer colors, all are returned. If no valid colors are found, it returns None.
        Args:
            color_string (str): A string containing color names separated by commas or ampersands.
        Returns:
            str | None: A string of up to the first two colors separated by commas, or None if
            the input is invalid or no colors are found.
        """
        
        if not isinstance(color_string, str):  # Handle non-string cases
            return None  

        words = re.split(r'[,&]', color_string)
        words = [word.strip().lower() for word in words if word.strip()]
        
        # Select matched colors (first 2 if more than 2, all otherwise)
        matched_colors = [word for word in (words[:2] if len(words) > 2 else words)]
        
        return ", ".join(matched_colors) if matched_colors else None
    
    @staticmethod
    def get_diff_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """
        Computes the difference between two DataFrames by returning rows that are 
        present in the first DataFrame (df1) but not in the second DataFrame (df2).
        Args:
            df1 (pd.DataFrame): The first DataFrame.
            df2 (pd.DataFrame): The second DataFrame.
        Returns:
            pd.DataFrame: A DataFrame containing rows that are unique to df1.
        """

        return df1.merge(df2, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

    @staticmethod
    def group_by_f2_colors(df2: pd.DataFrame, GROUP_FOLDER_PATH: str) -> None:
        """
        Groups a DataFrame by the 'f2_colors' column and saves each group as a separate CSV file.
        Args:
            df2 (pd.DataFrame): The input DataFrame containing a column named 'f2_colors'.
            GROUP_FOLDER_PATH (str): The directory path where the grouped CSV files will be saved.
        Returns:
            None
        Side Effects:
            - Saves grouped DataFrames as CSV files in the specified folder.
            - Prints the number of unique colors and the total number of rows in the input DataFrame.
            - Prints the location where the grouped CSV files are saved.
        Notes:
            - The filenames of the saved CSV files are generated based on the color name, with spaces 
              and special characters replaced by underscores or other substitutions.
            - The filenames also include the number of rows in each group.
        """
        
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
        """
        Reads CSV files from the specified directory, extracts color combination 
        and count information from the filenames, and returns the data as a 
        pandas DataFrame.
        The filenames are expected to follow the format: `<color_combo>_<count>.csv`, 
        where `<color_combo>` is a string representing a combination of colors 
        (with underscores as separators), and `<count>` is an integer.
        Args:
            file_path (str): The path to the directory containing the CSV files.
        Returns:
            pd.DataFrame: A DataFrame with two columns:
                - "color_combo": The color combination extracted from the filename, 
                  with underscores replaced by spaces.
                - "count": The integer count extracted from the filename.
        """
        
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
        """
        Splits a DataFrame into two based on a threshold and combines smaller groups into an "Other" category.
        Args:
            grouped_df (pd.DataFrame): A DataFrame containing grouped data with a "count" column.
            threshold (int, optional): The minimum count value to include in the main DataFrame. 
                                        Groups with counts below this value are combined into "Other". 
                                        Defaults to 10.
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: 
                - The first DataFrame contains groups with counts above or equal to the threshold, 
                  including an "Other" row for combined smaller groups.
                - The second DataFrame contains groups with counts below the threshold.
        """
        
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
        """
        Plots a bar chart to visualize color combinations and their row counts.
        Parameters:
        -----------
        df_final : pd.DataFrame
            A DataFrame containing the final aggregated data with columns:
            - "color_combo": The color combination names.
            - "count": The count of rows for each color combination.
        df_below : pd.DataFrame
            A DataFrame containing additional details for the "Other" category,
            specifically the color combinations that were grouped into "Other".
        Returns:
        --------
        None
            This function does not return any value. It displays a bar chart.
        Notes:
        ------
        - The bar corresponding to the "Other" category (if present) is highlighted
          in a different color (light coral) and annotated with the number of
          combinations it represents.
        - The x-axis labels are rotated for better readability.
        """
        
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
