import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

# setup webdriver
URL = "http://orteil.dashnet.org/experiments/cookie/"
service_obj = Service("C:\chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)
driver.get(URL)

#compose selenium actions
cookie = driver.find_element(By.ID, "cookie")
items = driver.find_elements(By.CSS_SELECTOR, "#store b")
item_prices = []
item_names = []
item_dic = {}
affordable_items = {}
timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes
while True:
    cookie.click()
    if time.time() > timeout:
        my_money = driver.find_element(By.ID, "money").text
        cookie_counts = int(my_money.replace(",", ""))
        print(cookie_counts)
        for item in items:
            item_text = item.text
            if item_text != "":
                cost = int(item_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
                name = item_text.split("-")[0]
                item_names.append(name)
                for n in range(len(item_prices)):
                    item_dic[item_names[n]] = item_prices[n]
        for key, value in item_dic.items():
            if cookie_counts > value:
                affordable_items[key] = value
        highest_available_item = max(affordable_items).strip()
        driver.find_element(By.ID, f"buy{highest_available_item}").click()
        timeout = time.time() + 5
    if time.time() > five_min:
        break

# for item_price in item_prices:
#     print(item_price.text)
# timeout_start = time.time()
# while time.time() < timeout_start + timeout:
#     cookie.click()
