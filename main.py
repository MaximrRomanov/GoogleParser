import os.path
import time
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
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
    options = Options()
    options.page_load_strategy = 'normal'
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    href_dict = {}
    result = []
    DOMAIN = 'webcache.googleusercontent.com'
    next_page_link = get_next_page_link_for_keyword(keywords, browser) # получили список ссылок на след стр по ключу
    count = 0
    for page in range(0,2):
        for keyword in keywords:
            if page == 0:
                url = 'https://www.google.com/search?q=' + keyword
                try:
                    browser.get(url)
                    dns = browser.find_elements(By.XPATH, '//div[@class="yuRUbf"]//a')
                    href_dict = {i + 1: dns[i].get_attribute('href') for i in range(0, len(dns))}
                except Exception as ex:
                    logging.exception(ex)

            else :
                url = next_page_link[]
                try:
                    browser.get(url)
                    dns = browser.find_elements(By.XPATH,'//div[@class="yuRUbf"]//a')
                    href_dict = {i+1: dns[i].get_attribute('href') for i in range(0, len(dns))}
                except Exception as ex:
                    logging.exception(ex)

            href_dict = check_for_webcache(href_dict, DOMAIN)# словарь с сайтами без рекламы
            print(f"Page is: {page+1}   query is: ")
            for key, value in href_dict.items():
                 print(f"{key} : {value}")

            dict_res = {}
            for domain in domain_list:
                for key,value in href_dict.items():
                    if value.startswith(domain, 8):
                      dict_res[key] = value
            result.append(dict_res)
            time.sleep(randrange(2,5))  # пауза между запросами, спасение от бана или капчи

    if browser:
        browser.quit()
    return result

def get_next_page_link_for_keyword(keywords: list, browser) -> list:
    next_page_link = []
    for keyword in keywords:
        url =  'https://www.google.com/search?q=' + keyword
        try:
            browser.get(url)
            next_page_link.append(browser.find_element(By.XPATH, '//td[@class="d6cvqb BBwThe"]//a[@id="pnnext"]').get_attribute(
                'href'))

        except Exception as ex:
            logging.exception(ex)
    return next_page_link


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
        ' zov-krasnodar.ru',
         'maikop.mebelister.ru',
         'zovmoscow.ru',
         'zovrus.ru',
        'leroymerlin.ru'
     ]

    region_title = 'Краснодар'
    result = parse(domain_list, get_keywords_list(query_list))
    print('Позиция сайта на странице:')
    print(result) # TODO: вывод в формате json

main()
'https://www.google.com/search?q=%D0%BA%D1%83%D1%85%D0%BD%D0%B8+%D0%B7%D0%BE%D0%B2&ei=BuTgY_bfMLmIxc8P9YCt4As&start=10&sa=N&ved=2ahUKEwj2-qL75ID9AhU5RPEDHXVAC7wQ8tMDegQIBxAE&biw=929&bih=927'
# 'https://www.google.com/search?q=%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C+%D0%BA%D1%83%D1%85%D0%BD%D1%8E&sxsrf=AJOqlzUf-zOPzBfmqjLHum_LH7MOzbi_2Q:1675682041231&ei=-eDgY_TlDb2Vxc8PrumwuAo&start=10&sa=N&ved=2ahUKEwi0xsuG4oD9AhW9SvEDHa40DKc4HhDy0wN6BAgEEAY&biw=1280&bih=671&dpr=1.5' 222
# 'https://www.google.com/search?q=%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C+%D0%BA%D1%83%D1%85%D0%BD%D1%8E&sxsrf=AJOqlzVEBcFFMNKgPqVUKfJz37EEHmApwg:1675682036773&ei=9ODgY5fsLpeGxc8PkM2XmAg&start=30&sa=N&ved=2ahUKEwiXtruE4oD9AhUXQ_EDHZDmBYM4FBDy0wN6BAgEEAk&biw=1280&bih=671&dpr=1.5' 444