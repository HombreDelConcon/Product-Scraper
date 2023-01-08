#------PYTHON LIBRARIES---------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging
import os
import time
from time import gmtime, strftime
#-------PERSONAL LIBRARIES------------------------------
from prodScraper import scrapeDataNewegg
from prodScraper import scrapeDataAMZ
from prodScraper import scrapeDataTarget


#UPDATED: 11/28/2022

#---------------IMPORTANT--------------------------------------------------------

#   To run the code in this file or the scraper file in a virtual environment or a regular
#   directory, the following libraries have to be installed:
#       - selenium
#       - webdriver_manager
#       - bs4
#       - lxml
#       - requests
#       - tkinter
#       - customtkinter


#Will access the main page of Amazon and start its traversal there and return a URL with the
#   results page
def getKeywordAMZMain(keyword: str) -> str:
    if keyword == None:
        return None
    #Webdriver_manager automatically logs to the terminal by default so these will disable
    # the logging to the terminal
    os.environ['WDM_LOCAL'] = 'false'
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    #Stores function name for database storing
    funcName = 'getKeywordAMZMain'
    
    #Starts up the driver which we will use to traverse the sites
    try:

        #Add in options to the driver like headless mode so that the browser window will not pop up
        options = Options()
        #options.add_argument('headless')
        options.add_argument('start_maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        search = None

        #Attempt to use one Amazon URL, since amazon tends to rotate URLs at times, this attempts to use one 
        #   URL and if it doesn't work then it attempts to use another 
        try:
            driver.get('https://www.amazon.com/ref=nav_logo')
            #Searches for the element containing the search bar
            search = driver.find_element(By.ID, 'twotabsearchtextbox')
        except:
            #_sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'AMZ: Error with Amazon URL, attmepting to use differnt URL')
            driver.get('https://www.amazon.com/')
            #Searches for the element containing the search bar
            search = driver.find_element(By.ID, 'twotabsearchtextbox')

        #Search bar string
        keyString = keyword

        time.sleep(4)

        #Types it on the search bar and hits ENTER 
        search.send_keys(keyString)
        time.sleep(1)
        search.send_keys(Keys.RETURN)

    except Exception as e:
        print(e)
        return None

    #Waits until the page has loaded for a maz of 10 seconds and takes a screenshot
    try:
        #Waits until a specific element in the page has loaded in then wait some extra time for everything else to load
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sg-col-inner')))
        time.sleep(5)
        driver.save_screenshot('shots\Shot1.png')

        #stores the current URL
        curURL = driver.current_url
          
    except Exception as e:
        return None

    else:
        driver.close()
        return curURL

#Will access the main page of Newegg and start its traversal there and return a URL with the
#   results page
def getKeywordNeweggMain(keyword: str) -> str:
    if keyword == None:
        return None
    #Webdriver_manager automatically logs to the terminal by default so these will disable
    # the logging to the terminal
    os.environ['WDM_LOCAL'] = 'false'
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    #Starts up the driver which we will use to traverse the sites
    try:
        options = Options()
        #options.add_argument('headless')
        options.add_argument('start_maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        driver.get('https://www.newegg.com/')

        time.sleep(5)

        #Searches for the element containing the search bar
        search = driver.find_element(By.TAG_NAME, 'input')

        #Search bar string
        keyString = keyword

        #Types it on the search bar and hits ENTER 
        search.send_keys(keyString)
        search.send_keys(Keys.RETURN)

    except Exception as e:
        return None

    #Waits until the page has loaded for a maz of 10 seconds then waits another 5 seconds 
    try:
        #Waits until a specific element in the page has loaded in
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'item-cell')))

        time.sleep(5)
        driver.save_screenshot('shots\Shot2.png')

        #stores the current URL
        curURL = driver.current_url
          
    except Exception as e:
        return None

    else:
        driver.close()
        return curURL

#Will access the main page of Target and start its traversal there and return a URL with the
#   results page
def getKeywordTargetMain(keyword: str) -> str:
    if keyword == None:
        return None
    #Webdriver_manager automatically logs to the terminal by default so these will disable
    # the logging to the terminal
    os.environ['WDM_LOG'] = 'false'
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    #Stores function name for database storing
    funcName = 'getKeywordTargetMain'
  
    try:
        options = Options()
        #options.add_argument('headless')
        options.add_argument('start maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        driver.get('https://www.target.com/')

        search = driver.find_element(By.TAG_NAME, 'input')
        time.sleep(3)
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)
    except Exception as e:
        return None

    try:
        time.sleep(5)
        driver.save_screenshot('shots\Shot3.png')
        curURL = driver.current_url

    except Exception as e:
        return None

    else:
        driver.quit()
        return(curURL)

#return date
def _getDate():
    date = strftime('%m-%d-%y', gmtime())
    return date

#Return time
def _getTime():
    time = strftime('%H:%M:%S')
    return time

#Main function containing all of the code from the main program

"""def main():
    print('Please input a keyword:')
    keyword = input()
    scraperInstance = _instantiate()
    funcName = 'Main'
    if _is_in_db(keyword):
        n = _get_info_by_kw(keyword)
        return n
    else:
        try:
            neweggURL = getKeywordNeweggMain(keyword, scraperInstance)
            amazonURL = getKeywordAMZMain(keyword, scraperInstance)
            targetURL = getKeywordTargetMain(keyword, scraperInstance)
        except Exception as e:
            ExcepT= e
            fExcepT = 'MNF:%s' % ExcepT
            _sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', fExcepT)
        else:
            totalProdsNewegg = scrapeDataNewegg(neweggURL, scraperInstance, keyword)
            totalProdsAMZ = scrapeDataAMZ(amazonURL, scraperInstance, keyword)
            totalProdsTarget = scrapeDataTarget(targetURL, keyword, scraperInstance)
            print('Amazon URL: ' + str(amazonURL))
            print('Newegg URL: ' + str(neweggURL))
            print('Target URL: ' + str(targetURL))
            return (totalProdsNewegg, totalProdsAMZ, totalProdsTarget)"""

if __name__ == '__main__':
    getKeywordNeweggMain('table')

    
