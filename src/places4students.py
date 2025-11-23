from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.places4students.com/schools/1255/listings/properties?pagination=1"

driver = webdriver.Chrome()
driver.get(url)

html = None
data = {
    "ID": [],
    "Description": [],
    "Distance": [],
    "Rooms": [],
    "Washrooms": [],
    "Price": [],
}

try:
    html = driver.page_source

except TimeoutException:
    print("Failed to load in time.")

driver.switch_to.default_content()
driver.quit()

if html:
    soup = BeautifulSoup(html, "html.parser")
    listings = soup.find_all("div", class_="group")
    listings = filter(None, listings)
    for listing in listings:
        desc = listing.find("h3")
        content = listing.find_all("span")
        content = list(filter(lambda c: c.text != "NEW", content))
        if desc and content:
            data["ID"].append(content[0].text)
            data["Description"].append(desc.text)
            data["Distance"].append(content[1].text)
            data["Price"].append("WIP")
            data["Rooms"].append(content[2].text)
            data["Washrooms"].append(content[3].text)

    df = pd.DataFrame(
        data,
    )
    print(df)
