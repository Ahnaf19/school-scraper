from bs4 import BeautifulSoup


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
    tr_all = tbody.find_all("tr")
    if not tr_all:
        print("No <tr> elements found in <tbody>")
        return {'issue': "No <tr> elements found in <tbody>"}

    tr_all_5 = tr_all[:5].copy()  # Limit to the first 5 rows
    
    school_name = tr_all_5[0].text.split('(')[0].strip()
    address = tr_all_5[1].text.strip() + ' ' + tr_all_5[2].text.strip()
    colors = tr_all_5[3].text.split(':')[1].strip()
    mascot = tr_all_5[4].text.split(':')[1].strip()

    data = {
        "school_name": str(school_name),
        "address": str(address),
        "mascot": str(mascot),
        "colors": str(colors)
    }
    
    return data
    

if __name__ == "__main__":
    print(get_data())