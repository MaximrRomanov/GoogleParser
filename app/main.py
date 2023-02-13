import time
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
from random import randrange
# from seleniumwire import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) Chrome/77.0.3865.90 Safari/537.36"')
    selenium_wire_options = {
        'addr': 'django',
        'proxies': {
            "http": "socks5://1fnvs1zk:q6q7fran@dina.ltespace.com:13574",
            "https": "socks5://1fnvs1zk:q6q7fran@dina.ltespace.com:13574",
            'no_proxy': 'localhost,django,127.0.0.1'
        }
    }

    browser = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return browser


def get_keywords_list(queryList: list) -> list:
    keywords = []
    if not queryList:
        logging.exception("QueryList is null")
        exit(1)

    for query in queryList:
        keywords.append(query.lower().replace(" ", "+"))

    return keywords


def get_position(domain_list: list, keywords: list) -> list:
    browser = init_driver()
    href_dict = {}
    result = []
    count_get = 0
    next_page_link = []
    for page in range(1, 4):
        count = 0
        for keyword in keywords:
            url = 'https://www.google.com/search?q=' + keyword if page < 3 else next_page_link[count]
            try:
                browser.get(url)
                time.sleep(randrange(2, 5))  # пауза между запросами, спасение от бана или капчи
                count_get += 1
                browser.get_screenshot_as_file(f"resource/{count_get}.png")
                print("----------------")
                print(count)
                print("----------------")
                if page == 2:
                    browser.get_screenshot_as_file(f"resource/next_2page_link{count_get}.png")
                    next_page_link.append(
                        browser.find_element(By.XPATH, '//td[@class="d6cvqb BBwThe"]//a[@id="pnnext"]').get_attribute(
                            'href'))

                    browser.get(next_page_link[count])
                    print(f"Count: {count} url: {next_page_link[count]}")

                elif page == 3:
                    browser.get_screenshot_as_file(f"resource/next_3page_link{count_get}.png")
                    next_page_link[count] = browser.find_element(By.XPATH,
                                                                 '//td[@class="d6cvqb BBwThe"]//a[@id="pnnext"]').get_attribute(
                        'href')  # заменил ссылку на вторую страницу ссылкой на третью

                    browser.get(next_page_link[count])
                    print(f"Count: {count} url: {next_page_link[count]}")

                dns = browser.find_elements(By.XPATH, '//div[@class="yuRUbf"]//a[@data-ved]')
                href_dict = {i + 1: dns[i].get_attribute('href') for i in range(0, len(dns))}
            except Exception as ex:
                logging.exception(ex)

            count += 1
            print(f"Page is: {page}")
            for key, value in href_dict.items():
                print(f"{key} : {value}")

            dict_res = {}
            for domain in domain_list:
                for key, value in href_dict.items():
                    if value.startswith(domain, 8):
                        dict_res[key] = value

            result.append(dict_res)
            time.sleep(randrange(2, 5))  # пауза между запросами, спасение от бана или капчи
    if browser:
        browser.quit()

    return result


def check_for_webcache(href_dict: dict) -> dict:
    href_dict = {key: value for key, value in href_dict.items() if
                 not value.startswith('webcache.googleusercontent.com', 8) and not value.startswith('www.google.com',
                                                                                                    8)}
    return href_dict


def main():
    query_list = [
        'кухни зов ',
        'купить кухни',
        'популярные crm системы'
    ]

    domain_list = [
        'zov01.ru',
        'zov-krasnodar.ru',
        'maikop.mebelister.ru',
        'zovmoscow.ru',
        'zovrus.ru',
        'leroymerlin.ru',
        'mebelveb.ru',
        'mas-mebel.ru',
        'mebelpik.ru'
    ]

    result = get_position(domain_list, get_keywords_list(query_list))
    print('Позиция сайта на странице:')
    print(result)  # TODO: вывод в формате json


main()
