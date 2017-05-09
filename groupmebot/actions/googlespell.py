from selenium import webdriver
from const import *
import urllib
import signal

#Initialize the phantomJS driver
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver.set_window_size(1120,550)

def findTypo(search_query):
    #Query Google to see if it has any suggestions
    driver.get("http://www.google.com/search?client=ubuntu&q=" + urllib.quote(search_query))
    [correct] = driver.find_elements_by_xpath(SPELL_TAG) or [None]
    if correct:
        return correct.text
    else:
        return

def killDriver():
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()
