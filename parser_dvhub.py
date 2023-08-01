from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}


def get_source_html(site_url):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1200x600")
    options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    count_pages = 1
    data = []

    try:
        driver.get(url=site_url)
        time.sleep(2)
        while True:
            try:
                print(f"[PROGRESS] Page in work: {count_pages}...")
                companies = driver.find_elements(By.CLASS_NAME, "company-wrap")
                for company in companies:
                    url = company.find_element(By.CLASS_NAME, "company__header") \
                        .find_element(By.TAG_NAME, "a").get_attribute("href")
                    get_items(url, data)
                try:
                    driver.find_element(By.ID, "link-next").click()
                    count_pages += 1

                except NoSuchElementException:
                    print("[INFO] Last page reached successfully")
                    break
            except Exception as _ex:
                print(_ex)
    except Exception as _ex:
        print(_ex)
    finally:
        with open("sources_dvhub/result_vl.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("[INFO] Data collected successfully!")
        driver.close()
        driver.quit()


def get_items(url, data):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1200x600")
    options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "show-contacts-block__link").click()
        item = driver.find_element(By.CLASS_NAME, "j_addressCol")

        try:
            item_name = driver.find_element(By.CLASS_NAME, "company-name-wrap").text
        except Exception as _ex:
            item_name = None

        try:
            item_email = driver.find_element(By.CLASS_NAME, "email").text
        except Exception as _ex:
            item_email = None

        try:
            item_website = driver.find_element(By.CLASS_NAME, "website").text
        except Exception as _ex:
            item_website = None

        try:
            item_phone = driver.find_elements(By.CLASS_NAME, "phone-wrap")
            item = []
            for phone in item_phone:
                item.append(phone.text)
            item_phone = item
        except Exception as _ex:
            item_phone = None

        try:
            item_address = driver.find_elements(By.CLASS_NAME, "address-string")
            item = []
            for address in item_address:
                item.append(address.text)
            item_address = item
        except Exception as _ex:
            item_address = None

        data.append(
            {
                "item_name": item_name,
                "item_url": url,
                "item_email": item_email,
                "item_phone": item_phone,
                "item_address": item_address,
                "item_site": item_website,
            }
        )
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    # url = 'https://www.dvhab.ru/khabarovsk/medicine-beauty/dentals'
    url = 'https://www.vl.ru/vladivostok/medicine-beauty/dentals'
    get_source_html(url)
