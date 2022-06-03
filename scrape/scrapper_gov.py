import requests
import threading
import time

import bs4
import yaml
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

GOV_BASE_ADDRESS = r"https://www.sejm.gov.pl"
GOV_REPR_ADDRESS = r"/sejm9.nsf/poslowie.xsp?type="

with open(f".\\data\\header_translation.yaml", "r", encoding="utf-8") as f:
    HEADER_TRANSLATION = yaml.safe_load(f)


def find_representatives(parsed_page: bs4.element.Tag) -> bs4.element.ResultSet:
    return parsed_page.find("div", {"id": "title_content"}).find_all("li")


def get_dynamic_items(sup_link: str, driver: webdriver.Chrome, container: dict):
    driver.get(GOV_BASE_ADDRESS + sup_link)
    voting_element = driver.find_element_by_id("glosowania")
    voting_element.click()
    WebDriverWait(driver, 10).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "view:_id1:_id2:facetMain:_id189:holdGlosowania"), "głosowaniach"
        )
    )
    percentage = driver.find_element_by_id(
        "view:_id1:_id2:facetMain:_id189:holdGlosowania"
    ).text.split()[3]
    container["voting_participation"] = float(percentage[:-1])


def analyze_repr_page(sup_link: str, driver: webdriver.Chrome) -> dict:
    repr_data = {}
    dyn_thread = threading.Thread(
        target=get_dynamic_items, args=(sup_link, driver, repr_data)
    )
    dyn_thread.start()
    repr_page = requests.get(GOV_BASE_ADDRESS + sup_link)
    parsed = bs4.BeautifulSoup(repr_page.content, "html.parser")
    base_data = (
        parsed.find("div", {"class": "partia"})
        .find("ul", {"class": "data"})
        .find_all("li")
    )
    cv_data = (
        parsed.find("div", {"class": "cv"}).find("ul", {"class": "data"}).find_all("li")
    )
    for item in base_data + cv_data:
        tag = item.find("p", {"class": "left"}).get_text().strip().replace(":", "")
        tag = HEADER_TRANSLATION.get(tag, tag)
        record = item.find("p", {"class": "right"}).get_text().strip()
        if tag == "Data i miejsce urodzenia":
            birth = record
            if "," in record:
                birth, city = record.split(", ")
                repr_data["city_of_birth"] = city
            repr_data["date_of_birth"] = birth
        elif tag == "constituency":
            district_id, constituency = record.split(maxsplit=1)
            repr_data["district_id"] = district_id
            repr_data["constituency_city"] = constituency
        else:
            repr_data[tag] = record
    dyn_thread.join()
    return repr_data


def analyze_repr_item(item: bs4.element.Tag, driver: webdriver.Chrome) -> dict:
    name = item.find("div", {"class": "deputyName"}).get_text().strip()
    party = item.find("strong").get_text().strip()
    add_info = item.find("strong").next_sibling.next_sibling
    href = item.find("a").get("href")
    repr_data = analyze_repr_page(href, driver)
    repr_data["name"] = name
    repr_data["party_short"] = party
    if add_info.name:
        add_info = add_info.next_sibling
    repr_data["additional_info"] = add_info.strip() if add_info else None
    return repr_data


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    gov_page = requests.get(GOV_BASE_ADDRESS + GOV_REPR_ADDRESS)
    parsed = bs4.BeautifulSoup(gov_page.content, "html.parser")
    representatives = find_representatives(parsed)

    all_repr_data = []
    for i, r in enumerate(representatives):
        print(f"Scrapping {i:>3}/{len(representatives)}\r", end="")
        all_repr_data.append(analyze_repr_item(r, driver))
    print("Scrapping finished!")

    driver.close()
    df = pd.DataFrame(all_repr_data)
    df.to_csv("..\\data\\repr.csv", index=False)
    df.to_excel("..\\data\\repr.xlsx", index=False)


if __name__ == "__main__":
    main()
