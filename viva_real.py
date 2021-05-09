#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
from tqdm import tqdm
from datetime import datetime

driver = webdriver.Chrome(ChromeDriverManager().install())

urls_dict = {"Brooklin": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/brooklin/apartamento_residencial/",
             "Butanta": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/butanta/apartamento_residencial/",
             "Republica": "https://www.vivareal.com.br/venda/sp/sao-paulo/centro/republica/apartamento_residencial/",
             "Bras": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-leste/bras/apartamento_residencial/",
             "Fregesia do O": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-norte/freguesia-do-o/apartamento_residencial/",
             "Higienopolis": "https://www.vivareal.com.br/venda/sp/sao-paulo/centro/higienopolis/apartamento_residencial/",
             "Jardins": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/jardins/apartamento_residencial/",
             "Lapa": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/lapa/apartamento_residencial/",
             "Moema": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/moema/apartamento_residencial/",
             "Mooca": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-leste/mooca/apartamento_residencial/",
             "Morumbi": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/morumbi/apartamento_residencial/",
             "Pinheiros": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/pinheiros/apartamento_residencial/",
             "Santana": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-norte/santana/apartamento_residencial/",
             "Saude": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/saude/apartamento_residencial/",
             "Vila Mariana": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/vila-mariana/apartamento_residencial/",
             "Vila Matilde": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-leste/vila-matilde/apartamento_residencial/",
             "Campo limpo": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/campo-limpo/apartamento_residencial/",
             "Tucuruvi": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-norte/tucuruvi/apartamento_residencial/"}

errors = []
results = []

for bairro, url in urls_dict.items():
    current_url = url
    driver.get(url)
    sleep(2)
    actions = ActionChains(driver)

    try:
        driver.find_element_by_class_name("cookie-notifier__cta").click()
    except:
            print("No cookies!")

    for i in tqdm(range(30), desc=bairro):

        sleep(5)
        main_div = driver.find_element_by_class_name("results-main__panel")
        properties = main_div.find_elements_by_class_name("js-property-card")
        paginator = driver.find_element_by_class_name("js-results-pagination")
        next_page = paginator.find_element_by_xpath("//a[@title='Próxima página']")

        for i,apartment in enumerate(properties):
            url = apartment.find_element_by_class_name("js-card-title").get_attribute("href")
            apto_id = url.split("id-")[-1][:-1]
            header = apartment.find_element_by_class_name("property-card__title").text
            address = apartment.find_element_by_class_name("property-card__address").text
            area = apartment.find_element_by_class_name("js-property-card-detail-area").text
            rooms = apartment.find_element_by_class_name("js-property-detail-rooms").text
            bathrooms = apartment.find_element_by_class_name("js-property-detail-bathroom").text
            garages = apartment.find_element_by_class_name("js-property-detail-garages").text
            try:
                amenities = apartment.find_element_by_class_name("property-card__amenities").text
            except:
                amenities = None
                errors.append(url)
            price = apartment.find_element_by_class_name("js-property-card-prices").text
            try:
                condo = apartment.find_element_by_class_name("js-condo-price").text
            except:
                condo = None
                errors.append(url)
            crawler = bairro
            crawled_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            results.append({"id": apto_id,
                            "url": url,
                            "header": header,
                            "address": address,
                            "area": area,
                            "rooms": rooms,
                            "bathrooms": bathrooms,
                            "garages": garages,
                            "amenities": amenities,
                            "price": price,
                            "condo": condo,
                            "crawler": crawler,
                            "crawled_at": crawled_at})
        next_page.click()
pd.DataFrame(results).to_csv("full_results.csv", index=False)
driver.close()


