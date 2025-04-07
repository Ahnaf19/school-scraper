from bs4 import BeautifulSoup
from loguru import logger as log


def get_data(soup: BeautifulSoup | None = None) -> dict[str, str]:
    
    if not soup:
        # Read the saved HTML file
        with open("data/table.html", "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

    # Find the table body
    tbody = soup.find("tbody")
    if not tbody:
        print("No <tbody> found in table.html")
        return {'issue': "No <tbody> found in table.html"}

    # Find all <tr> elements
    tr_all = tbody.find_all("tr") # type: ignore
    if not tr_all:
        print("No <tr> elements found in <tbody>")
        return {'issue': "No <tr> elements found in <tbody>"}
    
    # school_name extraction
    school_name = tr_all[0].text.split('(')[0].strip()
    log.info(f"{school_name}")

    # address extraction (handles the dynamic number of rows)
    address = ""
    found_colors_or_mascot = False  # Flag to indicate whether we've found "Colors" or "Mascot"

    # Iterate through tr_all from index 1 onwards
    for i in range(1, len(tr_all)):
        # If we encounter a row starting with "Colors" or "Mascot", stop and skip adding to address
        if tr_all[i].text.startswith("Colors") or tr_all[i].text.startswith("Mascot"):
            found_colors_or_mascot = True
            break
        # Add the current row text to the address if we haven't encountered "Colors" or "Mascot"
        address += tr_all[i].text.strip() + " "

    address = address.strip()  # Clean up extra spaces
    log.info(f"Address: {address if address else 'N/A'}")  # Handle empty address case

    # Colors extraction (handling if no "Colors" row exists)
    colors = "N/A"  # Default value for colors
    for i in range(1, len(tr_all)):
        if tr_all[i].text.startswith("Colors"):
            colors = tr_all[i].text.split(":")[1].strip()  # Extract colors after ":"
            break
    log.info(f"Colors: {colors}")

    # Mascot extraction (handling if no "Mascot" row exists)
    mascot = "N/A"  # Default value for mascot
    for i in range(1, len(tr_all)):
        if tr_all[i].text.startswith("Mascot"):
            mascot = tr_all[i].text.split(":")[1].strip()  # Extract mascot after ":"
            break
    log.info(f"Mascot: {mascot}")

    
    data = {
        "school_name": str(school_name),
        "address": str(address),
        "mascot": str(mascot),
        "colors": str(colors)
    }
    
    return data
    

if __name__ == "__main__":
    print(get_data())