import os.path
import time
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
import json
from random import randrange
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def generate_fake_ua() -> UserAgent:
    ua = UserAgent()
    return ua.random


def get_keywords_list(queryList: list) -> list:
    keywords = []
    if not queryList:
        logging.exception("QueryList is null")
        exit(1)
    for query in queryList:
        keywords.append(query.lower().replace(" ", "+"))
    return keywords


def parse(domain_list: list, keywords: list):
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    href_dict = {}
    result = []
    DOMAIN = 'webcache.googleusercontent.com'
    for page in range(0,1):
        for keyword in keywords:
            if page == 0:
                url = 'https://www.google.com/search?q=' + keyword
            else:
                url = 'https://www.google.com/search?q=' + keyword
            try:
                browser.get(url)
                dns = browser.find_elements(
                    By.XPATH,'//div[@class="yuRUbf"]//a')

                href_dict = {i+1: dns[i].get_attribute('href') for i in range(0, len(dns))}
            except Exception as ex:
                logging.exception(ex)

            href_dict = check_for_webcache(href_dict, DOMAIN)# словарь с сайтами без рекламы
            for key, value in href_dict.items():
                 print(f"{key} : {value}")

            # dict_res = {}
            # for domain in domain_list:
            #     for key,value in href_dict.items():
            #         if value.startswith(domain, 8):
            #           dict_res[key] = value
            # result.append(dict_res)
            time.sleep(randrange(2,5))  # пауза между запросами, спасение от бана или капчи

    if browser:
        browser.quit()


def check_for_webcache(href_dict, domain_ad) -> dict:
    href_dict = {key: value for key, value in href_dict.items() if not value.startswith(domain_ad, 8)}
    return href_dict


def main():
    query_list  =  [
        'кухни зов ',
        'купить кухни'
        ]

    domain_list = [
         'zov01.ru',
         '023-kuhni-lime.ru',
         'maikop.mebelister.ru',
         'vk.com',
         'zovrus.ru'
     ]

    region_title = 'Краснодар'
    result = parse(domain_list, get_keywords_list(query_list))
    print('Позиция сайта на странице:')
    print(result) # TODO: вывод в формате json

main()