from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time


def process_li(li: WebElement):
    try:
        # li_text = li.text.strip()
        # print(li_text)
        li.click()
        time.sleep(8)
        ul_info = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/div/div/ul"
        )
        # img_src = ul_info.find_element(By.TAG_NAME, "img").get_attribute("src")
        # print(ul_info.text)
        file.write(ul_info.text.strip() + "\n")
        # print(img_src)
        close_btn = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/footer/button"
        )
        close_btn.click()
        time.sleep(2)
    except:
        time.sleep(10)
        process_li(li)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://eng.iotexpo.com.cn/sz/ExhibitorList.html?hallNo=9")

time.sleep(10)  # Adjust the sleep time as necessary

ul_element = driver.find_element(By.ID, "co-main-ct")
li_elements = ul_element.find_elements(By.TAG_NAME, "li")


with open("output.txt", "a", encoding="utf-8") as file:
    for li in li_elements:
        process_li(li)


time.sleep(30)
driver.quit()
