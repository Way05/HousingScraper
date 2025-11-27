from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

url = "https://www.places4students.com/"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
data = {
    # "ID": [],
    "Description": [],
    # "Distance": [],
    "Bedrooms": [],
    "Bathrooms": [],
    "Price ($)": [],
}


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
            data["Bedrooms"].append(content[2].text)
            data["Bathrooms"].append(content[3].text)
            count += 1


def getData(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("ul", class_="flex flex-row items-center gap-1")
    if not pagination:
        scrapePage(soup)
    else:
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


def getSchoolPage(name):
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(1)
        searchBar = driver.find_element(By.TAG_NAME, "input")
        searchBar.send_keys(name)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@class='p-4 pb-2 border-b border-gray-200']",
                )
            )
        )
        time.sleep(1)
        searchResults = driver.find_element(By.TAG_NAME, "ul")
        schools = searchResults.find_elements(By.TAG_NAME, "li")
        print("Search results:")
        for i in range(len(schools)):
            print(f"({i + 1}) {schools[i].text.replace("\n", ", ")}")
        selection = input("Select school: ")
        print(f"Selected: {schools[int(selection) - 1].text.replace("\n", ", ")}")
        print("Scraping pages...")
        schools[int(selection) - 1].click()
        time.sleep(1)
        # get past cookies
        cookies = driver.find_element(
            By.XPATH,
            "//*[@class='text-white px-6 py-2 rounded-lg text-sm font-semibold shadow hover:opacity-90 transition-opacity']",
        )
        time.sleep(1)
        cookies.click()
        # click to listings
        listings = driver.find_element(
            By.XPATH, "//button[contains(text(), 'View Details')]"
        )
        listings.click()
        time.sleep(2)

        return getData(driver)
    except KeyboardInterrupt:
        print("Exiting by CTRL-C")
    finally:
        if driver:
            driver.quit()
