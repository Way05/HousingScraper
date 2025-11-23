from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

url = "https://www.places4students.com/schools/1255/listings/properties?pagination=1"
html = None
data = {
    # "ID": [],
    "Description": [],
    # "Distance": [],
    "Rooms": [],
    # "Washrooms": [],
    "Price ($)": [],
}


def getSchoolPage(name):
    # get search bar
    # type
    # get results
    # pick result
    # update url
    # scrape
    pass


def scrapePage(newSoup):
    listings = newSoup.find_all("div", class_="group")
    listings = filter(None, listings)
    prices = newSoup.find_all("div", class_="text-lg font-bold")
    count = 0
    for listing in listings:
        desc = listing.find("h3")
        content = listing.find_all("span")
        content = list(filter(lambda c: c.text != "NEW", content))
        if desc and content:
            # data["ID"].append(content[0].text)
            data["Description"].append(desc.text)
            # data["Distance"].append(content[1].text)
            data["Price ($)"].append(prices[count].text)
            data["Rooms"].append(content[2].text)
            # data["Washrooms"].append(content[3].text)
            count += 1


def getData():
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("ul", class_="flex flex-row items-center gap-1")
    pagination = pagination[0].find_all("li")[1:-1]
    for i in range(1, len(pagination) + 1):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, str(i)))
            )
            driver.find_element(By.LINK_TEXT, str(i)).click()

            time.sleep(3)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            scrapePage(soup)
        except NoSuchElementException:
            print("End of pages.")
            break

    driver.switch_to.default_content()
    driver.quit()

    return data
