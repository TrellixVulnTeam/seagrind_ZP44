import requests
import argparse
import driver
import pathlib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def get_silent_webdriver():
    driver.get_geckodriver()
    options = Options()
    options.headless = True
    gecko = webdriver.Firefox(
        options=options,
        executable_path='./driver/geckodriver')
    return gecko


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--contract', help='Contract address', required=True)
    parser.add_argument('-s', '--start-id', help='Starting token ID', required=True)
    parser.add_argument('-e', '--end-id', help='Ending token ID', required=True)
    args = vars(parser.parse_args())

    start_id, end_id, contract = args['start_id'], args['end_id'], args['contract']
    geckodriver = get_silent_webdriver()

    for token_id in range(int(start_id), int(end_id) + 1):
        try:
            geckodriver.get(f"https://opensea.io/assets/{contract}/{token_id}")
            elems = geckodriver.find_elements(By.XPATH, "//meta[contains(@content, 'lh3')]")
            url = elems[0].get_attribute("content")
            pathlib.Path(f'./{contract}/').mkdir(exist_ok=True)
            with open(f'./{contract}/{token_id}.png', 'wb') as f:
                f.write(requests.get(url, allow_redirects=True).content)
        except Exception as e:
            print(e)
            continue

    geckodriver.quit()
