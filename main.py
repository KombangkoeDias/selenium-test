from selenium import webdriver
from enum import Enum
import time
import os

os.environ['MOZ_HEADLESS'] = '1'

class tokens(Enum):
    MATIC = "MATIC"
    LINK = "LINK"

def faucet(token, address):
    try:
        driver = webdriver.Remote("http://localhost:4444")
        #driver = webdriver.Firefox()
        driver.get("https://faucet.matic.network/")

        if token == tokens.MATIC:
            radioElement = driver.find_element_by_css_selector("input[type='radio'][value='maticToken']")
            radioElement.click()
        elif token == tokens.LINK:
            radioElement = driver.find_element_by_css_selector("input[type='radio'][value='link']")
            radioElement.click()
        else:
            print("unsupported token")
            return

        radioElement = driver.find_element_by_css_selector("input[type='radio'][value='mumbai']")
        radioElement.click()

        input = driver.find_element_by_css_selector("input[type='text'][placeholder='Enter your account address']")
        input.send_keys(address)

        buttons = driver.find_elements_by_css_selector("button")
        for button in buttons:
            if button.get_attribute("innerHTML") == "Submit":
                button.click()
                break
        time.sleep(3)
        buttons = driver.find_elements_by_css_selector("button")
        for button in buttons:
            if button.get_attribute("innerHTML") == "Confirm":
                button.click()
                break
        time.sleep(5)

        texts = driver.find_elements_by_css_selector("p.card-header-title")
        found = False
        for text in texts:
            if text.get_attribute("innerHTML") == "Tx success:":
                found = True
                print("The transaction is success")
                links = driver.find_elements_by_css_selector("a[target='_blank']")
                for link in links:
                    href = link.get_attribute('href')
                    if href[:35] == 'https://mumbai-explorer.matic.today':
                        print("transaction link: https://mumbai.polygonscan.com/tx/" + href[39:])
                        return
                return
        if not found:
            print("The transaction doesn't seem to be success")
            cardHeaders = driver.find_elements_by_css_selector("p.card-header-title")
            for header in cardHeaders:
                if header.get_attribute('innerHTML') == 'Error':
                    parent = header.parent
                    content = parent.find_element_by_css_selector("div.card-content")
                    print("Reason:",content.get_attribute("innerHTML"))

    except Exception as e:
        print("Error:", e)

faucet(tokens.LINK, "0xf5751Aef65a4ED92C109f045964a5B0C6cf7E1Fe")