from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import json

STATE_PATH = "state.json"


def read_state():
    with open(STATE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_state(data):
    with open(STATE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def create_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def process_li(li: WebElement, n: int):
    try:
        # li_text = li.text.strip()
        # print(li_text)
        li.click()
        time.sleep(3)
        ul_info = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/div/div/ul"
        )
        # img_src = ul_info.find_element(By.TAG_NAME, "img").get_attribute("src")
        # print(ul_info.text)
        with open(f"output-{n}.txt", "a", encoding="utf-8") as file:
            file.write(ul_info.text.strip() + "\n")
        # print(img_src)
        close_btn = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/footer/button"
        )
        close_btn.click()
        time.sleep(1)
        return True
    except:
        return False
        # if n >= 10:
        #     return
        # time.sleep(10)
        # print(f"Reprocessing {n}")
        # process_li(li, n + 1)


service = Service(ChromeDriverManager().install())
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
        if time.time() - start_time > 300:
            driver.quit()
            driver = create_driver()
            start_time = time.time()
            driver.get(url)
            time.sleep(10)

        title = li.text.strip()
        if title in state[str(i)]["list"]:
            continue

        processed = process_li(li, i)
        if processed:
            state[str(i)]["list"].append(title)
            write_state(state)

    time.sleep(20)

driver.quit()
