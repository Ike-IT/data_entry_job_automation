from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import requests

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.8563026328125%2C%22east%22%3A-122.0103553671875%2C%22south%22%3A37.50887198616936%2C%22north%22%3A38.04075429569201%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

header = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

response = requests.get(url=ZILLOW_URL, headers=header)
data = response.text
# print(data)

soup = BeautifulSoup(data, "html.parser")
# print(soup.text)

"""Below code fetches the url links"""
rent_links = soup.select(selector=".dRjxkR a")
# print(rent_links)
all_links = []
for link in rent_links:
    href = link["href"]
    # print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
# print(all_links)

"""Below code fetches the addresses"""
all_addresses = soup.select(selector="#grid-search-results address")
address_list = [address.getText().split(" | ")[-1] for address in all_addresses]
# print(address_list)

"""Below code fetches the prices"""
all_prices = soup.select(selector="article span")
price_list = [price.get_text().split("+")[0].split("/")[0] for price in all_prices if "$" in price.text]
# print(price_list)


"""Below block of codes uses selenium 2 update my google docs"""
GOOGLE_DOC_URL = "https://docs.google.com/forms/d/17NNqZVxQOM8EVZXQXERdMrOefns7Jyz0ydAFFsbQjy8/edit"

""" D blocks of codes below prevents D browser 4rm closing automatically """
options = Options()
options.AddExcludedArgument("enable-automation")
options.add_experimental_option("detach", True)

SERVICE_OBJ = Service("\C:\Development\chromedriver_win32")
driver = webdriver.Chrome(service=SERVICE_OBJ, options=options)


for n in range(len(all_links)):
    driver.get(GOOGLE_DOC_URL)

    time.sleep(5)
    address_input_field = driver.find_element(By.XPATH,
                                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input_field.click()
    address_input_field.send_keys(address_list[n])
    price_input_field = driver.find_element(By.XPATH,
                                            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input_field.click()
    price_input_field.send_keys(price_list[n])
    url_link_field = driver.find_element(By.XPATH,
                                         '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    url_link_field.click()
    url_link_field.send_keys(all_links[n])
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()