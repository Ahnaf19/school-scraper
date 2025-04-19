# School Scraping

## 📚 Overview

The **School Scraping** is a Python-based tool designed to automate the collection, processing, and analysis of school-related data. The project focuses on web scraping, data extraction, color-based sorting, and visualization. It provides a streamlined pipeline to scrape school data, process it based on business logic, and generate meaningful insights.

Its a **freelancing work** that I did and so saved the source code for future referece.

> Developed on: python 3.10.16

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Loguru](https://img.shields.io/badge/loguru-FF9C00?style=for-the-badge&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

## 🚀 Features

- **Web Scraping**: Automates the extraction of school-related data from websites.
- **Data Cleaning**: Handles missing values and filters rows based on specific criteria.
- **Color Categorization**: Matches colors in the dataset against a predefined set of reference colors.
- **Grouping and Aggregation**: Groups data by categorized colors and generates grouped CSV files.
- **Visualization**: Creates visualizations of color combinations based on thresholds.
- **Interactive Notebook**: Provides a Jupyter Notebook for exploratory data analysis and debugging.

---

## 📂 Project Structure

```
school_scraping/
│
├── data/                     # Folder for input and output CSV files
│   ├── school_data.csv       # Input dataset
│   ├── school_data_diff.csv  # Filtered dataset with differences
│   └── grouped_data3/        # Folder for grouped CSV files
│
├── src/                      # Source code for the project
│   ├── colorsort.py          # Main script for data processing and visualization
│   ├── web_automation.py     # Automates web interactions for data collection
│   ├── scraper.py            # Extracts school-related data from websites
│   └── utils/                # Utility functions for color sorting and analysis
│
├── school_scraping.ipynb     # Jupyter Notebook for exploratory data analysis
├── requirements.txt          # Python dependencies for the project
├── LICENSE                   # License file for the project
└── README.md                 # Project documentation
```

---

## 🛠️ Key Components

### 1. **`colorsort.py`**

The main script that processes and visualizes the data:

- Reads the input dataset (`school_data.csv`).
- Filters rows based on a predefined set of reference colors.
- Categorizes colors into functional groups (`f2_colors`).
- Groups data by categorized colors and saves grouped CSV files.
- Visualizes color combinations using thresholds.

### 2. **`web_automation.py`**

A script for automating web interactions:

- Navigates to school-related websites.
- Automates form submissions, button clicks, and other interactions.
- Saves raw HTML or extracted data for further processing.

### 3. **`scraper.py`**

A script for extracting data from websites:

- Parses HTML content using libraries like `BeautifulSoup`.
- Extracts relevant school-related data (e.g., names, locations, colors).
- Saves the extracted data into structured formats (e.g., CSV files).

### 4. **`school_scraping.ipynb`**

A Jupyter Notebook for exploratory data analysis:

- Provides an interactive environment for debugging and testing.
- Demonstrates the end-to-end workflow of the project.
- Useful for visualizing intermediate steps and outputs.

### 5. **`requirements.txt`**

A file listing all Python dependencies required for the project:

- Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

---

## 📊 Workflow

1. **Web Automation**: Use `web_automation.py` to automate interactions with school-related websites and collect raw data.
2. **Data Scraping**: Use `scraper.py` to parse and extract relevant data from the collected HTML.
3. **Input Data**: The extracted data is saved as `school_data.csv` in the `data/` folder.
4. **Data Cleaning**: Run `colorsort.py` to clean and filter the dataset.
5. **Color Filtering**: Colors are matched against a predefined set of reference colors (e.g., "Black", "Blue", "Red").
6. **Grouping**: Data is grouped by categorized colors and saved as CSV files in the `grouped_data3` folder.
7. **Visualization**: Color combinations are visualized based on a threshold to highlight significant patterns.

---

## 📥 Input Files

- **`school_data.csv`**: The primary dataset containing school-related data, including a `colors` column.
- **Raw HTML Files**: Collected by `web_automation.py` for parsing by `scraper.py`.

---

## 📤 Output Files

- **`school_data_diff.csv`**: A filtered dataset containing rows that match the reference colors.
- **`grouped_data3/`**: A folder containing grouped CSV files based on categorized colors.
- **Extracted Data Files**: Structured data files (e.g., CSV) generated by `scraper.py`.

---

## 📈 Visualizations

The script generates visualizations of color combinations:

- **`df_final`**: Displays significant color combinations above the threshold.
- **`df_below`**: Highlights color combinations below the threshold.

---

## 🛠️ How to Run

1. **Install Dependencies**:

   - Install the required Python packages using:
     ```bash
     pip install -r requirements.txt
     ```

2. **Web Automation**:

   - Run `web_automation.py` to collect raw data from school-related websites:
     ```bash
     python src/web_automation.py
     ```

3. **Data Scraping**:

   - Run `scraper.py` to extract relevant data from the collected HTML:
     ```bash
     python src/scraper.py
     ```

4. **Data Processing**:

   - Place the extracted data (`school_data.csv`) in the `data/` folder.
   - Run `colorsort.py` to process and visualize the data:
     ```bash
     python src/colorsort.py
     ```

5. **Interactive Analysis**:

   - Open `school_scraping.ipynb` in Jupyter Notebook for exploratory data analysis:
     ```bash
     jupyter notebook school_scraping.ipynb
     ```

6. **Check Outputs**:
   - Processed data and visualizations will be saved in the `data/` folder.

---

## 📋 Reference Colors

The script uses a predefined set of reference colors for filtering and categorization:

```
Black, Blue, Brown, Burgundy, Cardinal, Carolina Blue, Columbia Blue, Crimson, Dark Gray,
Dark Green, Forest Green, Gold, Gray, Green, Hunter Green, Kelly Green, Lime, Light Blue,
Light Pink, Magenta, Maroon, Navy, Neon Green, Neon Yellow, Old Gold, Orange, Pink, Purple,
Red, Royal Blue, Scarlet, Silver, Sports Yellow, Teal, Vegas Gold, White, Yellow
```

---

## 🌟 Future Enhancements

- Add support for dynamic reference color lists.
- Improve visualization with interactive dashboards.
- Extend web scraping to include additional data sources.

---

## 📧 Contact

For questions or suggestions, feel free to reach out!
