import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}


def get_source_html(url):
    driver = webdriver.Chrome()

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)

        while True:
            try:
                find_more_element = driver.find_element(By.CLASS_NAME, "button-show-more")
                time.sleep(3)
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(find_more_element).click().perform()
                    time.sleep(3)
                except:
                    print("[Info] Webpage is loading")
            except EC.NoSuchElementException:
                print("[Info] Page downloaded succesfully")
                with open("source.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_items_urls(file_path):
    with open(file_path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="minicard-item__container")

    urls = []
    for item in items_divs:
        item_url = item.find("h2", class_="minicard-item__title").find("a").get("href")
        urls.append(item_url)

    with open("items_urls.txt", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collected successfully!"


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]

    result_list = []
    urls_count = len(urls_list)
    count = 1
    for url in urls_list:
        try:
            response = requests.get(url=url, headers=headers)
        except:
            # time.sleep(random.randrange(60,65))
            time.sleep(random.randrange(10,15))
            response = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")

        try:
            item_name = soup.find("span", {"itemprop": "name"}).text.strip()
        except Exception as _ex:
            item_name = None

        item_phones_list = []
        try:
            item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")

            for phone in item_phones:
                item_phone = phone.get("href").split(":")[-1].strip()
                item_phones_list.append(item_phone)
        except Exception as _ex:
            item_phones_list = None

        try:
            item_address = soup.find("address", class_="iblock").text.strip()
        except Exception as _ex:
            item_address = None

        # try:
        #     item_site = soup.find(string=re.compile("Сайт|Официальный сайт")).find_next().text.strip()
        # except Exception as _ex:
        #     item_site = None

        result_list.append(
            {
                "item_name": item_name,
                "item_url": url,
                "item_phones_list": item_phones_list,
                "item_address": item_address,
            }
        )

        time.sleep(random.randrange(5, 10))

        if count % 10 == 0:
            time.sleep(random.randrange(10, 15))

        print(f"[+] Current progress: {count}/{urls_count}")

        count += 1

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    return "[INFO] Data collected successfully!"


if __name__ == "__main__":
    site_url = 'https://vladivostok.zoon.ru/medical/?search_query_form=1&m%5B520398a5a0f302e571000013%5D=1&districts%5B%5D=pervomajskij&districts%5B%5D=leninskij&districts%5B%5D=pervorechenskij&districts%5B%5D=rybachij&districts%5B%5D=sovetskij&districts%5B%5D=frunzenskij&districts%5B%5D=schitovaya'
    # get_source_html(url=site_url)
    # print(get_items_urls(file_path="source.html"))
    print(get_data(file_path="items_urls.txt"))
