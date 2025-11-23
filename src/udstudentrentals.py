from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

url = "https://www.udstudentrentals.com/availableproperties"
html = None
data = {"Location": [], "Price": [], "Tenants": [], "Status": []}


def getData():
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        time.sleep(1)
        scroll_amount = 1000  # Adjust this value based on your page's layout
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        # print(f"Scrolled iframe document down by {scroll_amount} pixels.")

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "nKphmK"))
        )
        # print("iframe found")
        # driver.switch_to.frame(iframe)
        # print("switched to iframe")

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            # EC.visibility_of_element_located((By.ID, "theTable"))
            # EC.visibility_of_element_located((By.XPATH, "//*[@id='theTable']"))
            EC.presence_of_element_located((By.XPATH, "//*[@id='theTable']//tbody"))
        )
        # print("table found")

        html = driver.page_source

    except TimeoutException:
        print("Failed to load in time.")

    driver.switch_to.default_content()
    driver.quit()

    if html:
        soup = BeautifulSoup(html, "html.parser")
        listings = soup.find_all("tr")
        for i in range(len(listings)):
            details = listings[i].find_all("td")
            for i in range(0, len(details) - 3, 4):
                data["Location"].append(details[i].text)
                data["Price"].append(details[i + 1].text)
                data["Tenants"].append(details[i + 2].text)
                data["Status"].append(details[i + 3].text)

    return data
