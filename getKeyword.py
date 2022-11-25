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
#Log to database
from db_Interactions import _scraper_Logs as _sL
#Clear database tables
from db_Interactions import _clear_Table as _cT
#Keep track of which instance of the scrape is being run
from db_Interactions import _instantiate
#Check database before searching the web
from db_Interactions import _is_in_db, _get_info_by_kw


#UPDATED: 11/24/2022

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
def getKeywordAMZMain(keyword: str, inst: int) -> str:
    if keyword == None:
        return None
    #Webdriver_manager automatically logs to the terminal by default so these will disable
    # the logging to the terminal
    os.environ['WDM_LOCAL'] = 'false'
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    #Records the instance of the scraper for storing logs in the database
    scraperInstance = inst

    #Stores function name for database storing
    funcName = 'getKeywordAMZMain'
    
    #Starts up the driver which we will use to traverse the sites
    try:
        #_sL logs to the database (see db_Interactions.py)
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'INFO', 'AMZ:Starting Amazon scraper...')

        #Add in options to the driver like headless mode so that the browser window will not pop up
        options = Options()
        options.add_argument('headless')
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
            _sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'AMZ: Error with Amazon URL, attmepting to use differnt URL')
            driver.get('https://www.amazon.com/')
            #Searches for the element containing the search bar
            search = driver.find_element(By.ID, 'twotabsearchtextbox')

        #Search bar string
        keyString = keyword

        #Types it on the search bar and hits ENTER 
        search.send_keys(keyString)
        search.send_keys(Keys.RETURN)

    except Exception as e:
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'AMZ:Error in traversal')
        print(e)
        return None

    #Waits until the page has loaded for a maz of 10 seconds and takes a screenshot
    try:
        #Waits until a specific element in the page has loaded in
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sg-col-inner')))

        time.sleep(5)
        driver.save_screenshot('shots\Shot1.png')

        #stores the current URL
        curURL = driver.current_url
          
    except Exception as e:
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'AMZ:Error returning results')
        return None

    else:
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'INFO', 'AMZ:Traversal finished')

        driver.close()
        return curURL

#Will access the main page of Newegg and start its traversal there and return a URL with the
#   results page
def getKeywordNeweggMain(keyword, inst):
    if keyword == None:
        return None
    #Webdriver_manager automatically logs to the terminal by default so these will disable
    # the logging to the terminal
    os.environ['WDM_LOCAL'] = 'false'
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    #Records the instance of the scraper for storing logs in the database
    scraperInstance = inst

    #Stores function name for database storing
    funcName = 'getKeywordNeweggMain'

    #Starts up the driver which we will use to traverse the sites
    try:
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'INFO', 'NWG:Starting Newegg scraper')
        options = Options()
        options.add_argument('headless')
        options.add_argument('start_maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        driver.get('https://www.newegg.com/')

        #Searches for the element containing the search bar
        search = driver.find_element(By.TAG_NAME, 'input')

        #Search bar string
        keyString = keyword

        #Types it on the search bar and hits ENTER 
        search.send_keys(keyString)
        search.send_keys(Keys.RETURN)

    except Exception as e:
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'NWG:Error in traversal')
        return None

    #Waits until the page has loaded for a maz of 10 seconds and takes a screenshot
    try:
        #Waits until a specific element in the page has loaded in
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'item-cell')))

        time.sleep(5)
        driver.save_screenshot('shots\Shot2.png')

        #stores the current URL
        curURL = driver.current_url
          
    except Exception as e:
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'NWG:Error returning results')
        return None

    else:
        _sL(scraperInstance, _getDate(), _getTime(), funcName, 'INFO', 'NWG:Traversal finished')
        driver.close()
        return curURL

def getKeywordTargetMain(keyword: str, inst: int) -> str:
    if keyword == None:
        return None
    #Webdriver_manager automatically logs to the terminal by default so these will disable
    # the logging to the terminal
    os.environ['WDM_LOG'] = 'false'
    logging.getLogger('WDM').setLevel(logging.NOTSET)

    #Records the instance of the scraper for storing logs in the database
    scraperInstance = inst

    #Stores function name for database storing
    funcName = 'getKeywordTargetMain'
  
    try:
        #_sL(scraperInstance, _getDate(), _getTime(), funcName, 'INFO', 'TRG:Starting Target scraper')
        options = Options()
        #options.add_argument('headless')
        options.add_argument('start maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        driver.get('https://www.target.com/')

        search = driver.find_element(By.TAG_NAME, 'input')
        time.sleep(2)
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)
    except Exception as e:
        #_sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'TRG:Error in traversal')
        return None

    try:
        time.sleep(5)
        driver.save_screenshot('shots\Shot3.png')

        curURL = driver.current_url

    except Exception as e:
        #_sL(scraperInstance, _getDate(), _getTime(), funcName, 'ERROR', 'TRG:Error returning results')
        return None

    else:
        #_sL(scraperInstance, _getDate(), _getTime(), funcName, 'INFO', 'TRG:Traversal finished')
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

def main():
    print('Please input a keyword:')
    keyword = input()
    scraperInstance = _instantiate()
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
            return (totalProdsNewegg, totalProdsAMZ, totalProdsTarget)

if __name__ == '__main__':
    getKeywordTargetMain('Table', 2)

    
