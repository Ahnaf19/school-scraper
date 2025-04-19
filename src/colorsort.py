import pandas as pd

from .utils import ColorSort

def main():
    """
    Main function to process and analyze school color data.
    This function performs the following steps:
    1. Reads school data from a CSV file.
    2. Filters rows based on the presence of valid colors from a predefined set of reference colors.
    3. Saves the filtered data to a new CSV file.
    4. Assigns secondary color categories to the filtered data.
    5. Groups the data by these secondary color categories and saves the grouped data to separate CSV files.
    6. Reads the grouped data and identifies color combinations based on a specified threshold.
    7. Visualizes the identified color combinations.
    Constants:
        SCHOOL_DATA_PATH (str): Path to the input CSV file containing school data.
        DF_DIFF_PATH (str): Path to save the CSV file containing rows that were filtered out.
        GROUP_FOLDER_PATH (str): Path to save grouped data files.
    Dependencies:
        - Requires the `ColorSort` class with the following methods:
            - `isin_refcolors`: Checks if a color is in the reference color set.
            - `get_diff_df`: Computes the difference between two DataFrames.
            - `assign_f2_colors`: Assigns secondary color categories.
            - `group_by_f2_colors`: Groups data by secondary color categories and saves to files.
            - `read_group_data`: Reads grouped data from files.
            - `get_color_combos`: Identifies color combinations based on a threshold.
            - `plot_color_combos`: Visualizes color combinations.
    Returns:
        None
    """
    SCHOOL_DATA_PATH = "data/school_data.csv"
    DF_DIFF_PATH = "data/school_data_diff.csv"
    GROUP_FOLDER_PATH = "data/grouped_data3"

    df = pd.read_csv(SCHOOL_DATA_PATH)
    df = df.dropna(subset=['colors']).reset_index(drop=True)

    reference_colors = {
        "Black", "Blue", "Brown", "Burgundy", "Cardinal", "Carolina Blue", "Columbia Blue",
        "Crimson", "Dark Gray", "Dark Green", "Forest Green", "Gold", "Gray", "Green",
        "Hunter Green", "Kelly Green", "Lime", "Light Blue", "Light Pink", "Magenta",
        "Maroon", "Navy", "Neon Green", "Neon Yellow", "Old Gold", "Orange", "Pink",
        "Purple", "Red", "Royal Blue", "Scarlet", "Silver", "Sports Yellow", "Teal",
        "Vegas Gold", "White", "Yellow"
    }

    reference_colors_lower = {color.lower() for color in reference_colors}

    df2 = df[df['colors'].apply(lambda x: ColorSort.isin_refcolors(x, reference_colors_lower))] # * Filter rows where isin_refcolors returns True
    df2 = df2.reset_index(drop=True)

    # * Save the filtered DataFrame to a CSV file
    df_diff = ColorSort.get_diff_df(df, df2)
    df_diff.to_csv(DF_DIFF_PATH, index=False)

    df2["f2_colors"] = df2["colors"].apply(lambda x: ColorSort.assign_f2_colors(x))

    # * saving "group by" csv files
    ColorSort.group_by_f2_colors(df2, GROUP_FOLDER_PATH)

    grouped_df = ColorSort.read_group_data(GROUP_FOLDER_PATH)
    df_final, df_below = ColorSort.get_color_combos(grouped_df, threshold=10)

    # * visualize
    ColorSort.plot_color_combos(df_final, df_below)

if __name__ == "__main__":
    main()