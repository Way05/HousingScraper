from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

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
        print(desc)
        print(content)
        if desc and content:
            data["ID"].append(content[0].text)
            data["Description"].append(desc.text)
            data["Distance"].append(content[1].text)
            data["Price"].append(content[2].text)
            data["Rooms"].append(content[3].text)
            data["Washrooms"].append(content[4].text)

    df = pd.DataFrame(
        data,
    )
    df.set_index("ID")
    print(df)
