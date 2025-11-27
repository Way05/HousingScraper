from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

url = "https://www.udstudentrentals.com/availableproperties"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
data = {
    "Location": [],
    "Price ($)": [],
    "Tenants": [],
    "Bedrooms": [],
    "Bathrooms": [],
    # "Status": []
    "Link": [],
}


def getData():
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    mainHTML = None
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

        mainHTML = driver.page_source

        links = driver.find_elements(By.XPATH, "//a[@href='javascript:void(0)']")
        for i in range(len(links)):
            time.sleep(1)
            links = driver.find_elements(By.XPATH, "//a[@href='javascript:void(0)']")
            time.sleep(1)
            links[i].click()
            time.sleep(1)
            data["Link"].append(driver.current_url)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            h6 = soup.find_all("h6")
            rooms = next((t for t in h6 if "Bedroom" in t.text), None)
            brs = next((t for t in h6 if "Bathroom" in t.text), None)
            if rooms and brs:
                data["Bedrooms"].append(rooms.text)
                data["Bathrooms"].append(brs.text)
            else:
                data["Bedrooms"].append("Check Site")
                data["Bathrooms"].append("Check Site")
            driver.back()
            time.sleep(1)
            scroll_amount = 1000
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(1)
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "nKphmK"))
            )

    except TimeoutException:
        print("Failed to load in time.")

    driver.switch_to.default_content()
    driver.quit()

    if mainHTML:
        soup = BeautifulSoup(mainHTML, "html.parser")
        listings = soup.find_all("tr")
        for i in range(len(listings)):
            details = listings[i].find_all("td")
            for i in range(0, len(details) - 3, 4):
                data["Location"].append(details[i].text)
                data["Price ($)"].append(details[i + 1].text)
                data["Tenants"].append(details[i + 2].text)
                # data["Status"].append(details[i + 3].text)

    return data
