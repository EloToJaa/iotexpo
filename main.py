from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import json
import sys

STATE_PATH = "state.json"


def read_state():
    with open(STATE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_state(data):
    with open(STATE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


driver_path = ChromeDriverManager().install()


def create_driver():
    service = Service(driver_path)
    return webdriver.Chrome(service=service)


def process_li(li: WebElement, n: int):
    try:
        onclick = li.get_attribute("onclick")
        driver.execute_script(onclick)
        time.sleep(1.5)

        ul_info = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/div/div/ul"
        )
        with open(f"output-{n}.txt", "a", encoding="utf-8") as file:
            file.write(ul_info.text.strip() + "\n")
        close_btn = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/footer/button"
        )
        onclick = close_btn.get_attribute("onclick")
        driver.execute_script(onclick)
        time.sleep(0.5)

        return True
    except:
        return False


driver = create_driver()

state = read_state()
start_time = time.time()

for i in range(9, 13):
    url = f"https://eng.iotexpo.com.cn/sz/ExhibitorList.html?hallNo={i}"
    driver.get(url)

    time.sleep(10)

    ul_element = driver.find_element(By.ID, "co-main-ct")
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    state[str(i)]["max_counter"] = len(li_elements)

    for li in li_elements:
        title = li.text.strip()
        if title in state[str(i)]["list"]:
            print(f"Skipping: {title}")
            continue

        print(f"Processing: {title}")

        # if time.time() - start_time > 300:
        #     driver.quit()
        #     driver = create_driver()
        #     start_time = time.time()
        #     driver.get(url)
        #     time.sleep(10)

        processed = process_li(li, i)
        if processed:
            state[str(i)]["list"].append(title)
            write_state(state)

    time.sleep(20)

driver.quit()
