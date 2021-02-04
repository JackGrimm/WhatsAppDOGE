from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import requests
import re
import cryptocompare

chromepath = "C:\Python36\chromedriver_win32\chromedriver.exe"  # Selenium chromedriver path
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Kyle\\AppData\\Local\\Google\\Chrome\\User Data")
#Above is used to keep whatsapp logged in.
#options.add_argument("--headless") #Not working with whatsapp


def SendMessage (message, namelist):
    driver = webdriver.Chrome(executable_path=chromepath, chrome_options=options)
    driver.get("https://web.whatsapp.com/")

    while True:
        try:
            appLoad = driver.find_element_by_class_name("_1l12d")  #This class only exists after login
            if appLoad:
                break  #The login was successful
        except:
            time.sleep(1) #Wait for the page to load and retry

    for name in namelist:
        try:
            input_box_search = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')
            input_box_search.click()
            input_box_search.send_keys(name, Keys.ENTER)
            user = driver.find_element_by_xpath(f"//span[@title='{name}']")
            user.click()
            text_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            text_box.send_keys(message,Keys.ENTER)
        except:
            driver.close()
    time.sleep(1) #some messages aren't sent fast enough
    driver.close()


def check():
    while True:
        res = requests.get('https://jackgrimm.pythonanywhere.com/doge')
        soup = BeautifulSoup(res.text, 'html.parser')  # soup is now the html file
        target = str(soup.findAll("a", class_="DOGE"))
        target = target.split('[<a class="DOGE">')[1]
        target = target.split('</a>')[0]

        res = requests.get('https://coinmarketcap.com/currencies/dogecoin/')
        soup = BeautifulSoup(res.text, 'html.parser')  # soup is now the html file
        percentage = soup.findAll("span", class_="qe1dn9-0 RYkpI")
        percentage = re.findall("</span>[0-9][0-9].[0-9][0-9]<!-- -->", str(percentage))
        #NOTE: Need to see what a negative percentage is shown as, and code it in.  
        percentage = str(percentage[0])
        percentage = percentage.split('</span>')[1]
        percentage = percentage.split('<!-- -->')[0]

        compare = cryptocompare.get_price("DOGE",currency="USD")
        DOGE = float(compare['DOGE']['USD'])

        if DOGE >= float(target):
            SendMessage(f"Current Price is ${compare['DOGE']['USD']}. Daily change is {percentage}%", ["Kyle","Jc"])
        else:
            print(f"Target of {target} not met, as DOGE is {DOGE}.")
        time.sleep(60*10)

if __name__ == "__main__":
    check()
