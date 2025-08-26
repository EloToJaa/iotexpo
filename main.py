from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
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


driver_path = ChromeDriverManager().install()


def create_driver():
    service = Service(driver_path)
    return webdriver.Chrome(service=service)


def extract_li_text(li: WebElement) -> str:
    span_text = li.find_element(By.TAG_NAME, "span").text
    text = li.text.replace(span_text, "").strip()
    return text


def process_li(li: WebElement, title: str):
    try:
        onclick = li.get_attribute("onclick")
        driver.execute_script(onclick)
        time.sleep(3)

        ul_info = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/div/div/ul"
        )

        li_infos = ul_info.find_elements(By.TAG_NAME, "li")
        if len(li_infos) < 5:
            return []

        image_src = li_infos[0].find_element(By.TAG_NAME, "img").get_attribute("src")
        exhibitor_name = extract_li_text(li_infos[1])
        booth_number = extract_li_text(li_infos[2])
        company_address = extract_li_text(li_infos[3])
        company_introduction = extract_li_text(li_infos[4])

        close_btn = driver.find_element(
            By.XPATH, "/html/body/div[7]/div/div[1]/footer/button"
        )
        onclick = close_btn.get_attribute("onclick")
        driver.execute_script(onclick)
        time.sleep(1)

        return [
            title,
            exhibitor_name,
            booth_number,
            company_address,
            image_src,
            company_introduction,
        ]
    except:
        return []


driver = create_driver()

header_row = [
    "Company Name",
    "Exhibitor Name",
    "Booth Number",
    "Company Address",
    "Logo URL",
    "Company Introduction",
]
xlsx_data = [header_row]

state = read_state()

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

        processed = process_li(li, title)
        if len(processed) > 0:
            # xlsx_data.append(processed)
            state[str(i)]["list"].append(title)
            state[str(i)]["data"].append(processed)
            write_state(state)

    time.sleep(20)

driver.quit()
