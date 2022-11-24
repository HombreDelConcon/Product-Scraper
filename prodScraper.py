from bs4 import BeautifulSoup
import requests
#import pandas as pd
import json
import time
from db_Interactions import _store_product_info as _sp
from imageDownloader import _downloadImg as _dIMG
from imageDownloader import _clean_remainder as _cl

#_downloadImg(image_url, folder):
#_store_product_info(url, prod_name, prod_price, kw, retailer, image_path)

#Scrape product information from walmart main page
def scrapeDataWalmart(link, inst):
    if link == None:
        print('Nothing returned')
        return None

    else:
        #Stores extra information that will be store in the DB later
        retailerDB = 'Walmart'
        URLDB = link
        
        #Contains HTTP headers for scraper
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7", "Upgrade-Insecure-Requests": "1", "X-Amzn-Trace-Id": "Root=1-6292aed6-1f65c2db636f27cb7ebcb533"}
        URL = link
        webpage = requests.get(URL, headers=HEADERS)

        #Gets the HTML of the page and parses through it, also cleans it up
        soup = BeautifulSoup(webpage.content, 'lxml')
        soup2 = BeautifulSoup(soup.prettify(), 'lxml')


        #Stores the individual sections of product information
        containers = soup2.find_all('div', {'class': 'mb1 ph1 pa0-xl bb b--near-white w-25'})#'sans-serif mid-gray relative flex flex-column w-100'})

        #Stores the product names and prices is tuples
        productTups = []

        #Extracts the data from each container and turns it into a tuple to then store it
        for container in containers:
            try:
                #Just a comment to store tag information to copy and paste
                """
                price: div aria-hidden="true" class="b black f5 mr1 mr2-xl lh-copy f4-l"
                name: span class="w_At"
                """

                #Gets product name
                prodName = container.find('span', {'class':'w_At'}).get_text().strip()

                #Gets product price
                prodPrice = container.find('div', {'class':'b black f5 mr1 mr2-xl lh-copy f4-l'}).get_text().strip()

                tup = (prodName, prodPrice)
                print(tup)
            except AttributeError:
                pass

#Scrape product information from Amazon results page
def scrapeDataAMZ(link, inst, kw):
    #The traversal functions will return none if the url is None
    if link == None:
        print('Nothing returned')
        return None

    else:   
        URL = link
        #Contains HTTP headers for scraper 
        HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7", "Host": "httpbin.org", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36","X-Amzn-Trace-Id": "Root=1-62def870-3af35c732649e7f2796478a5"}
        webpage = requests.get(URL, headers=HEADERS)

        #Gets the HTML of the page and parses through it, also cleans it up
        soup = BeautifulSoup(webpage.content, 'lxml')
        soup2 = BeautifulSoup(soup.prettify(), 'lxml')
        #return soup2
        
        totalProds = 0
        totalExceptions = 0
        containers = None
        try:
            #Stores the individual sections of product information
            containers = soup2.find_all('div', {'class':'s-card-container s-overflow-hidden aok-relative s-expand-height s-include-content-margin s-latency-cf-section s-card-border'})
        except:
            pass
        else:
            if len(containers) != 0:
                images = soup2.find_all('img', {'class':'s-image'})
                
                print("AMAZON \n----------------------------------------------------------")
                #Extracts the data from each container and turns it into a tuple to then store it
                for container in containers:
                    try:
                        #Just a comment to store tag information to copy and paste
                        """
                        price: <span class="a-offscreen"></span>"
                        name: <span class="a-size-base-plus a-color-base a-text-normal"></span>"
                        """
                        
                        prodName = container.find('span', {'class':'a-size-base-plus a-color-base a-text-normal'}).get_text().strip()
                        prodPrice = container.find('span', {'class':'a-offscreen'}).get_text().strip()
                        prodImg = container.find('img', {'class':'s-image'})['src']
                        prodURL = container.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
                        prodKW = kw
                        prodRetailer = 'Amazon'
                        imgKey = _dIMG(str(prodImg), 'product_images_Amazon', prodName)
                        imgKey = None
                        tup = (prodName, prodPrice, prodImg, prodURL, prodKW, prodRetailer, imgKey)
                        _sp(prodURL, prodName, float(prodPrice.replace('$', '').replace(',', '')), prodKW, prodRetailer, imgKey)
                        print(tup)
                        print()
                        totalProds += 1

                    except AttributeError:
                        pass

        try:
            containers = soup2.find_all('div', {'class':'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
        except:
            pass
        else:
            if len(containers) != 0:
                images = soup2.find_all('img', {'class':'s-image'})

                print("AMAZON \n----------------------------------------------------------")
                #Extracts the data from each container and turns it into a tuple to then store it
                for container in containers:
                    try:
                        #Just a comment to store tag information to copy and paste
                        """
                        price: <span class="a-offscreen"></span>"
                        name: <span class="a-size-medium a-color-base a-text-normal"></span>"
                        """
            
                        prodName = container.find('span', {'class':'a-size-medium a-color-base a-text-normal'}).get_text().strip()
                        prodPrice = container.find('span', {'class':'a-offscreen'}).get_text().strip()
                        prodImg = container.find('img', {'class':'s-image'})['src']
                        prodURL = 'https://www.amazon.com' + str(container.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href'])
                        prodKW = kw
                        prodRetailer = 'Amazon'
                        imgKey = _dIMG(str(prodImg), 'product_images_Amazon', prodName)
                        imgKey = None 
                        tup = (prodName, prodPrice, prodImg, prodURL, prodKW, prodRetailer, imgKey)
                        _sp(prodURL, prodName, float(prodPrice.replace('$', '').replace(',', '')), prodKW, prodRetailer, imgKey)
                        print(tup)
                        print()
                        totalProds += 1

                    except AttributeError:
                        pass
        return totalProds
        #return soup2
    
def scrapeDataNewegg(link, inst, kw):
    if link == None:
        return None

    else:
        try:
            #Stores extra information that will be store in the DB later
            retailerDB = 'Newegg'
            URLDB = link

            #Contains HTTP headers for scraper
            HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7", "Upgrade-Insecure-Requests": "1", "X-Amzn-Trace-Id": "Root=1-6292aed6-1f65c2db636f27cb7ebcb533"}
            URL = link
            webpage = requests.get(URL, headers=HEADERS)

            #Gets the HTML of the page and parses through it, also cleans it up
            soup = BeautifulSoup(webpage.content, 'lxml')
            soup2 = BeautifulSoup(soup.prettify(), 'lxml')

            #Stores the individual sections of product information
            containers = soup2.find_all('div', {'class':'item-cell'})
            totalProds = 0
            print("NEWEGG \n----------------------------------------------------------")
            #Extracts the data from each container and turns it into a tuple to then store it
            for container in containers:
                try:
                    #Just a comment to store tag information to copy and paste
                    """
                    price: <li class="price-current">
                    name: <a class="item-title">
                    """

                    #Gets product name
                    prodName = container.find('a', {'class':'item-title'}).get_text().strip()
                    #Gets product price
                    prodPrice = container.find('li', {'class':'price-current'})#.get_text().strip()
                    bigPrice = prodPrice.find('strong', {}).get_text().strip()
                    lilPrice = prodPrice.find('sup', {}).get_text().strip()
                    totalPrice = '$' + bigPrice + lilPrice
                    prodURL = container.find('a', {'class':'item-title'})['href']
                    prodKW = kw
                    prodRetailer = 'Newegg'
                    prodImg = container.find('img', {'alt':prodName})['src']
                    imgKey = _dIMG(prodImg, 'product_images_Newegg', prodName)
                    _sp(prodURL, prodName, totalPrice.replace('$','').replace(',', ''), prodKW, prodRetailer, imgKey)

                    tup = (prodName, totalPrice, prodURL, prodImg, imgKey)
                    print(tup)
                    print()
                    totalProds += 1
                except AttributeError:
                    pass
            return totalProds
        except:
            return None

def scrapeDataTarget2(link, keyword):
    if link == None:
        print('Nothing returned')
        return None

    else:
        product_title = []
        price = []
        prodURL = []
        for i in range(0, 240, 24):
            cookies = {
                'TealeafAkaSid': 'nR3ZTRgUUMFQ4zx3yl7SLpaTB8AYfb9b',
                'visitorId': '0181304B93F30201A565CF06A8C9F398',
                'sapphire': '1',
                'UserLocation': '18201|40.950|-75.980|PA|US',
                'fiatsCookie': 'DSI_1845|DSN_Wilkes-Barre|DSZ_18702',
                'ci_pixmgr': 'other',
                'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwianRpIjoiVEdULmQ4MDU5OTBkZjE3ZDQxMGViYTdmYWNmMTA5ZDE5MTMyLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImMxNjNlNDM2NjQ5YTA3MDkzZWRlNWVhZjZjNjg1YWRhMTFkM2E5YmUxNjVhYjg1ZjdlMWUyYjBiNTcwMDFhNmYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.wYLz4oB447mjQme9eYFRoDS74W25bmIaDGMYgQcmFc4c9nGrVqbB5eGNuKooXeYtZfpN_TCPGUA72s2Y778qq5RoFndQNNVyCbSqUWp_7ZzYN7X0-ssePYFfoqoA2csKbfJjvfUcPDS1YjOzZhIjsyWsVxYdO6NRR1cmFzYem5osqEJEOu1nR-6d_uvQpvRRVjKL4JwgS3obqSFhBYjCo4J_58tWRH7X15SUPJMtyq2LLN2fLG4YQMiUrrueq5u3hxBj3wOWEpVHUmxdvSRJhCwbaFlmOPpb2bDUTNsjQVJy3IKQpMk7NdHpAQ-BlU91zM-UHktdQzl1H8RG0yNX8w',
                'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.',
                'refreshToken': 'kmiB85VDSJ6q-nwLTsR408V6Qh-wMSelkmNcUU2vwdfK4pfnpJFnTkIFgclOH8txJoI1I0AFQMImEf9Vz40rIQ',
                '_mitata': 'NjA0MjExZGY4YjI1NjI5NzdhNjFlMThmNzEyOTkyNzljMmZhODg4NGIyMzVhZjBjODQ5MGE2NTExZjlkMDMyNg==_/@#/1655964564_/@#/c4BfMEx7NHOksFe0_/@#/NjkwMzlkMTJjNjg0NGZlYjEwNTI4YzZhNjdiZjJjNTc1MWM0NzhiZGVlODcyZTZmNjNhMmRiNmVlMWFkMjAxMg==_/@#/000',
                'ffsession': '{%22sessionHash%22:%222dd4c68fbdda71655165155492%22%2C%22prevPageName%22:%22search:%20search%20results%22%2C%22prevPageType%22:%22search:%20search%20results%22%2C%22prevPageUrl%22:%22https://www.target.com/s?searchTerm=tv%22%2C%22sessionHit%22:20%2C%22prevSearchTerm%22:%22tv%22}',
            }

            headers = {
                'authority': 'redsky.target.com',
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
                # Requests sorts cookies= alphabetically
                # 'cookie': 'TealeafAkaSid=nR3ZTRgUUMFQ4zx3yl7SLpaTB8AYfb9b; visitorId=0181304B93F30201A565CF06A8C9F398; sapphire=1; UserLocation=18201|40.950|-75.980|PA|US; fiatsCookie=DSI_1845|DSN_Wilkes-Barre|DSZ_18702; ci_pixmgr=other; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwianRpIjoiVEdULmQ4MDU5OTBkZjE3ZDQxMGViYTdmYWNmMTA5ZDE5MTMyLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImMxNjNlNDM2NjQ5YTA3MDkzZWRlNWVhZjZjNjg1YWRhMTFkM2E5YmUxNjVhYjg1ZjdlMWUyYjBiNTcwMDFhNmYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.wYLz4oB447mjQme9eYFRoDS74W25bmIaDGMYgQcmFc4c9nGrVqbB5eGNuKooXeYtZfpN_TCPGUA72s2Y778qq5RoFndQNNVyCbSqUWp_7ZzYN7X0-ssePYFfoqoA2csKbfJjvfUcPDS1YjOzZhIjsyWsVxYdO6NRR1cmFzYem5osqEJEOu1nR-6d_uvQpvRRVjKL4JwgS3obqSFhBYjCo4J_58tWRH7X15SUPJMtyq2LLN2fLG4YQMiUrrueq5u3hxBj3wOWEpVHUmxdvSRJhCwbaFlmOPpb2bDUTNsjQVJy3IKQpMk7NdHpAQ-BlU91zM-UHktdQzl1H8RG0yNX8w; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=kmiB85VDSJ6q-nwLTsR408V6Qh-wMSelkmNcUU2vwdfK4pfnpJFnTkIFgclOH8txJoI1I0AFQMImEf9Vz40rIQ; _mitata=NjA0MjExZGY4YjI1NjI5NzdhNjFlMThmNzEyOTkyNzljMmZhODg4NGIyMzVhZjBjODQ5MGE2NTExZjlkMDMyNg==_/@#/1655964564_/@#/c4BfMEx7NHOksFe0_/@#/NjkwMzlkMTJjNjg0NGZlYjEwNTI4YzZhNjdiZjJjNTc1MWM0NzhiZGVlODcyZTZmNjNhMmRiNmVlMWFkMjAxMg==_/@#/000; ffsession={%22sessionHash%22:%222dd4c68fbdda71655165155492%22%2C%22prevPageName%22:%22search:%20search%20results%22%2C%22prevPageType%22:%22search:%20search%20results%22%2C%22prevPageUrl%22:%22https://www.target.com/s?searchTerm=tv%22%2C%22sessionHit%22:20%2C%22prevSearchTerm%22:%22tv%22}',
                'origin': 'https://www.target.com',
                'referer': 'https://www.target.com/s?searchTerm=' + str(keyword),
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            }

            params = {
                'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
                'channel': 'WEB',
                'count': '24',
                'default_purchasability_filter': 'true',
                'include_sponsored': 'true',
                'keyword': str(keyword),
                'offset': str(i),
                'page': '/s/' + str(keyword),
                'platform': 'desktop',
                'pricing_store_id': '1845',
                'store_ids': '1845,1474,1260,2536,2399',
                'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'visitor_id': '0181304B93F30201A565CF06A8C9F398',
            }

            url = 'https://www.target.com/s?searchTerm=' + str(keyword)

            page = requests.get(url)
            cookiesUpdate = page.cookies
            cookieStore = {}
            for c in cookiesUpdate:
                tempDict = {c.name: c.value}
                cookieStore.update(tempDict)
            newRefreshToken = refreshTokens(url)
            tempDict = {'refreshToken': str(newRefreshToken)}
            cookieStore.update(tempDict)
            cookies.update(cookieStore)
            
            response = requests.get('https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1', params=params, cookies=cookies, headers=headers)
            results_json = response.json()
            return results_json
            resultItems = results_json['data']['search']['products']

            for result in resultItems:
                try:
                    product_title.append(result['item']['product_description']['title'].replace('&#8482;', ''))
                except:
                    product_title.append('')

                try:
                    price.append(result['price']['formatted_current_price'])
                except:
                    price.append('')

                try:
                    prodURL.append(result['item']['enrichment']['buy_url'])
                except:
                    prodURL.append('Null')
        totalProducts = []
        try:
            for i in range(len(price)):
                totalProducts.append((product_title[i], price[i], prodURL[i]))
        except Exception as e:
            pass



        print('TARGET \n--------------------------------------------------------')
        for i in range(20):
            print(totalProducts[i])
            print()
            
        return totalProducts

def refreshTokens(url):
    if url == None:
        return None
    else:
        cookies = {
            'TealeafAkaSid': 'nR3ZTRgUUMFQ4zx3yl7SLpaTB8AYfb9b',
            'visitorId': '0181304B93F30201A565CF06A8C9F398',
            'sapphire': '1',
            'UserLocation': '18201|40.950|-75.980|PA|US',
            'fiatsCookie': 'DSI_1845|DSN_Wilkes-Barre|DSZ_18702',
            'ci_pixmgr': 'other',
            'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYyMTc2NTAsImlhdCI6MTY1NjEzMTI1MCwianRpIjoiVEdULmNkMjIxZTA1YTAyZjRhODc4NmJhODFkNjdiNjAyY2JmLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImMxNjNlNDM2NjQ5YTA3MDkzZWRlNWVhZjZjNjg1YWRhMTFkM2E5YmUxNjVhYjg1ZjdlMWUyYjBiNTcwMDFhNmYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.f6lWeClwCqwtmfuVQGjDrwVacsxbmvHyStfRzMHf2zd2j894UFtGk2mPtKEkKAvkkZ4LJL90R4XkggKMHpjxbDlzUi5gXv1S4aNGQ9A4kAsu0_j4xurOU8FV5FwARB6QhZ91gzpcON34e8ZOxU-x2i6inBuQ2LGpsws1eEnoHTptp1X8z7NYYrlmzQIJ6qG1YTuFbZef3PlDqlM1AkXC3ZJjeTpVaJ66VPnh6PWx8X92baa79lUcor88a3H5xU6ldMsPgCZOGEO99m6fYIcYN_RYz2i10R5pBk_e4THudZlhEEx1EjdTOcj1jwVrDdFdl-3_VdVFkt1Sc0ryruI7iA',
            'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYyMTc2NTAsImlhdCI6MTY1NjEzMTI1MCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.',
            #'refreshToken': 'qawZYOjSSlxuLmTk06qkk9c2UjU3QhwUauR4zkrGx38KkxPugdo9mjB5P9XK2Vu6UudrdmfTMnnMb0mfTlzpRQ',
            'refreshToken': 'kmiB85VDSJ6q-nwLTsR408V6Qh-wMSelkmNcUU2vwdfK4pfnpJFnTkIFgclOH8txJoI1I0AFQMImEf9Vz40rIQ',
            'ffsession': '{%22sessionHash%22:%222dd4c68fbdda71655165155492%22%2C%22prevPageName%22:%22search:%20search%20results%22%2C%22prevPageType%22:%22search:%20search%20results%22%2C%22prevPageUrl%22:%22https://www.target.com/s?searchTerm=flag%22%2C%22sessionHit%22:42%2C%22prevSearchTerm%22:%22flag%22}',
        }

        headers = {
            'authority': 'gsp.target.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'TealeafAkaSid=nR3ZTRgUUMFQ4zx3yl7SLpaTB8AYfb9b; visitorId=0181304B93F30201A565CF06A8C9F398; sapphire=1; UserLocation=18201|40.950|-75.980|PA|US; fiatsCookie=DSI_1845|DSN_Wilkes-Barre|DSZ_18702; ci_pixmgr=other; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYyMTc2NTAsImlhdCI6MTY1NjEzMTI1MCwianRpIjoiVEdULmNkMjIxZTA1YTAyZjRhODc4NmJhODFkNjdiNjAyY2JmLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImMxNjNlNDM2NjQ5YTA3MDkzZWRlNWVhZjZjNjg1YWRhMTFkM2E5YmUxNjVhYjg1ZjdlMWUyYjBiNTcwMDFhNmYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.f6lWeClwCqwtmfuVQGjDrwVacsxbmvHyStfRzMHf2zd2j894UFtGk2mPtKEkKAvkkZ4LJL90R4XkggKMHpjxbDlzUi5gXv1S4aNGQ9A4kAsu0_j4xurOU8FV5FwARB6QhZ91gzpcON34e8ZOxU-x2i6inBuQ2LGpsws1eEnoHTptp1X8z7NYYrlmzQIJ6qG1YTuFbZef3PlDqlM1AkXC3ZJjeTpVaJ66VPnh6PWx8X92baa79lUcor88a3H5xU6ldMsPgCZOGEO99m6fYIcYN_RYz2i10R5pBk_e4THudZlhEEx1EjdTOcj1jwVrDdFdl-3_VdVFkt1Sc0ryruI7iA; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYyMTc2NTAsImlhdCI6MTY1NjEzMTI1MCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=qawZYOjSSlxuLmTk06qkk9c2UjU3QhwUauR4zkrGx38KkxPugdo9mjB5P9XK2Vu6UudrdmfTMnnMb0mfTlzpRQ; ffsession={%22sessionHash%22:%222dd4c68fbdda71655165155492%22%2C%22prevPageName%22:%22search:%20search%20results%22%2C%22prevPageType%22:%22search:%20search%20results%22%2C%22prevPageUrl%22:%22https://www.target.com/s?searchTerm=flag%22%2C%22sessionHit%22:42%2C%22prevSearchTerm%22:%22flag%22}',
            'origin': 'https://www.target.com',
            'referer': str(url),
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }

        json_data = {
            'grant_type': 'refresh_token',
            'client_credential': {
                'client_id': 'ecom-web-1.0.0',
            },
            'device_info': {
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'language': 'en-US',
                'canvas': '229e4ce83af9c93f022bc5906a50b362',
                'color_depth': '24',
                'device_memory': '8',
                'pixel_ratio': 'unknown',
                'hardware_concurrency': '8',
                'resolution': '[1920,1080]',
                'available_resolution': '[1920,1040]',
                'timezone_offset': '240',
                'session_storage': '1',
                'local_storage': '1',
                'indexed_db': '1',
                'add_behavior': 'unknown',
                'open_database': '1',
                'cpu_class': 'unknown',
                'navigator_platform': 'Win32',
                'do_not_track': 'unknown',
                'regular_plugins': '["PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf","Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf","Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf","Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf","WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"]',
                'adblock': 'false',
                'has_lied_languages': 'false',
                'has_lied_resolution': 'false',
                'has_lied_os': 'false',
                'has_lied_browser': 'false',
                'touch_support': '[0,false,false]',
                'js_fonts': '["Arial","Arial Black","Arial Narrow","Calibri","Cambria","Cambria Math","Comic Sans MS","Consolas","Courier","Courier New","Georgia","Helvetica","Impact","Lucida Console","Lucida Sans Unicode","Microsoft Sans Serif","MS Gothic","MS PGothic","MS Sans Serif","MS Serif","Palatino Linotype","Segoe Print","Segoe Script","Segoe UI","Segoe UI Light","Segoe UI Semibold","Segoe UI Symbol","Tahoma","Times","Times New Roman","Trebuchet MS","Verdana","Wingdings"]',
                'navigator_vendor': 'Google Inc.',
                'navigator_webdriver': 'false',
                'navigator_app_name': 'Netscape',
                'navigator_app_code_name': 'Mozilla',
                'navigator_app_version': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'navigator_languages': '["en-US","es-US","es","en"]',
                'navigator_cookies_enabled': 'true',
                'navigator_java_enabled': 'false',
                'visitor_id': '0181304B93F30201A565CF06A8C9F398',
                'tealeaf_id': 'nR3ZTRgUUMFQ4zx3yl7SLpaTB8AYfb9b',
                'webgl': 'ee08404b371e98f59bcb7a01d444f375',
                'webgl_vendor': 'Google Inc. (NVIDIA)~ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                'browser_name': 'Unknown',
                'browser_version': 'Unknown',
                'cpu_architecture': 'Unknown',
                'device_vendor': 'Unknown',
                'device_model': 'Unknown',
                'device_type': 'Unknown',
                'engine_name': 'Unknown',
                'engine_version': 'Unknown',
                'os_name': 'Unknown',
                'os_version': 'Unknown',
            },
        }
        

        response = requests.post('https://gsp.target.com/gsp/oauth_tokens/v2/client_tokens', cookies=cookies, headers=headers, json=json_data)
        json_data = response.json()

        refreshToken = json_data['access_token']
        return refreshToken

def scrapeDataTarget(link, keyword, inst):
    if link == None:
        return None

    else:
        product_title = []
        price = []
        prodURL = []
        prodKW = keyword
        prodRetailer = 'Target'
        prodImg = []
        prodImgPath = []
        cap = 5
        for i in range(0, 240, 24):
            cookies = {
                'TealeafAkaSid': 'nR3ZTRgUUMFQ4zx3yl7SLpaTB8AYfb9b',
                'visitorId': '0181304B93F30201A565CF06A8C9F398',
                'sapphire': '1',
                'UserLocation': '18201|40.950|-75.980|PA|US',
                'fiatsCookie': 'DSI_1845|DSN_Wilkes-Barre|DSZ_18702',
                'ci_pixmgr': 'other',
                'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwianRpIjoiVEdULmQ4MDU5OTBkZjE3ZDQxMGViYTdmYWNmMTA5ZDE5MTMyLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImMxNjNlNDM2NjQ5YTA3MDkzZWRlNWVhZjZjNjg1YWRhMTFkM2E5YmUxNjVhYjg1ZjdlMWUyYjBiNTcwMDFhNmYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.wYLz4oB447mjQme9eYFRoDS74W25bmIaDGMYgQcmFc4c9nGrVqbB5eGNuKooXeYtZfpN_TCPGUA72s2Y778qq5RoFndQNNVyCbSqUWp_7ZzYN7X0-ssePYFfoqoA2csKbfJjvfUcPDS1YjOzZhIjsyWsVxYdO6NRR1cmFzYem5osqEJEOu1nR-6d_uvQpvRRVjKL4JwgS3obqSFhBYjCo4J_58tWRH7X15SUPJMtyq2LLN2fLG4YQMiUrrueq5u3hxBj3wOWEpVHUmxdvSRJhCwbaFlmOPpb2bDUTNsjQVJy3IKQpMk7NdHpAQ-BlU91zM-UHktdQzl1H8RG0yNX8w',
                'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.',
                'refreshToken': 'qawZYOjSSlxuLmTk06qkk9c2UjU3QhwUauR4zkrGx38KkxPugdo9mjB5P9XK2Vu6UudrdmfTMnnMb0mfTlzpRQ',
                '_mitata': 'NjA0MjExZGY4YjI1NjI5NzdhNjFlMThmNzEyOTkyNzljMmZhODg4NGIyMzVhZjBjODQ5MGE2NTExZjlkMDMyNg==_/@#/1655964564_/@#/c4BfMEx7NHOksFe0_/@#/NjkwMzlkMTJjNjg0NGZlYjEwNTI4YzZhNjdiZjJjNTc1MWM0NzhiZGVlODcyZTZmNjNhMmRiNmVlMWFkMjAxMg==_/@#/000',
                'ffsession': '{%22sessionHash%22:%222dd4c68fbdda71655165155492%22%2C%22prevPageName%22:%22search:%20search%20results%22%2C%22prevPageType%22:%22search:%20search%20results%22%2C%22prevPageUrl%22:%22https://www.target.com/s?searchTerm=tv%22%2C%22sessionHit%22:20%2C%22prevSearchTerm%22:%22tv%22}',
            }

            headers = {
                'authority': 'redsky.target.com',
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
                # Requests sorts cookies= alphabetically
                # 'cookie': 'TealeafAkaSid=nR3ZTRgUUMFQ4zx3yl7SLpaTB8AYfb9b; visitorId=0181304B93F30201A565CF06A8C9F398; sapphire=1; UserLocation=18201|40.950|-75.980|PA|US; fiatsCookie=DSI_1845|DSN_Wilkes-Barre|DSZ_18702; ci_pixmgr=other; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwianRpIjoiVEdULmQ4MDU5OTBkZjE3ZDQxMGViYTdmYWNmMTA5ZDE5MTMyLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImMxNjNlNDM2NjQ5YTA3MDkzZWRlNWVhZjZjNjg1YWRhMTFkM2E5YmUxNjVhYjg1ZjdlMWUyYjBiNTcwMDFhNmYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.wYLz4oB447mjQme9eYFRoDS74W25bmIaDGMYgQcmFc4c9nGrVqbB5eGNuKooXeYtZfpN_TCPGUA72s2Y778qq5RoFndQNNVyCbSqUWp_7ZzYN7X0-ssePYFfoqoA2csKbfJjvfUcPDS1YjOzZhIjsyWsVxYdO6NRR1cmFzYem5osqEJEOu1nR-6d_uvQpvRRVjKL4JwgS3obqSFhBYjCo4J_58tWRH7X15SUPJMtyq2LLN2fLG4YQMiUrrueq5u3hxBj3wOWEpVHUmxdvSRJhCwbaFlmOPpb2bDUTNsjQVJy3IKQpMk7NdHpAQ-BlU91zM-UHktdQzl1H8RG0yNX8w; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJjZWJjODJhMi01NWZkLTRjMGItYWNiNS0zY2E2ZGUzZjE4YjQiLCJpc3MiOiJNSTYiLCJleHAiOjE2NTYwMjAwMjksImlhdCI6MTY1NTkzMzYyOSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=kmiB85VDSJ6q-nwLTsR408V6Qh-wMSelkmNcUU2vwdfK4pfnpJFnTkIFgclOH8txJoI1I0AFQMImEf9Vz40rIQ; _mitata=NjA0MjExZGY4YjI1NjI5NzdhNjFlMThmNzEyOTkyNzljMmZhODg4NGIyMzVhZjBjODQ5MGE2NTExZjlkMDMyNg==_/@#/1655964564_/@#/c4BfMEx7NHOksFe0_/@#/NjkwMzlkMTJjNjg0NGZlYjEwNTI4YzZhNjdiZjJjNTc1MWM0NzhiZGVlODcyZTZmNjNhMmRiNmVlMWFkMjAxMg==_/@#/000; ffsession={%22sessionHash%22:%222dd4c68fbdda71655165155492%22%2C%22prevPageName%22:%22search:%20search%20results%22%2C%22prevPageType%22:%22search:%20search%20results%22%2C%22prevPageUrl%22:%22https://www.target.com/s?searchTerm=tv%22%2C%22sessionHit%22:20%2C%22prevSearchTerm%22:%22tv%22}',
                'origin': 'https://www.target.com',
                'referer': 'https://www.target.com/s?searchTerm=' + str(keyword),
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            }

            params = {
                'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
                'channel': 'WEB',
                'count': '24',
                'default_purchasability_filter': 'true',
                'include_sponsored': 'true',
                'keyword': str(keyword),
                'offset': str(i),
                'page': '/s/' + str(keyword),
                'platform': 'desktop',
                'pricing_store_id': '1845',
                'store_ids': '1845,1474,1260,2536,2399',
                'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'visitor_id': '0181304B93F30201A565CF06A8C9F398',
            }

            url = 'https://www.target.com/s?searchTerm=' + str(keyword)

            page = requests.get(url)
            cookiesUpdate = page.cookies
            cookieStore = {}
            for c in cookiesUpdate:
                tempDict = {c.name: c.value}
                cookieStore.update(tempDict)
            newRefreshToken = refreshTokens(url)
            tempDict = {'accessToken': str(newRefreshToken)}
            cookieStore.update(tempDict)
            cookies.update(cookieStore)
            
            response = requests.get('https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1', params=params, cookies=cookies, headers=headers)
            results_json = response.json()
            resultItems = results_json['data']['search']['products']

            for result in resultItems:
                temp_prod_title = None
                try:
                    product_title.append(result['item']['product_description']['title'].replace('&#8482;', ''))
                    temp_prod_title = result['item']['product_description']['title'].replace('&#8482;', '')
                except:
                    product_title.append('')
                try:
                    price.append(result['price']['formatted_current_price'])
                except:
                    price.append('')
                try:
                    prodURL.append(result['item']['enrichment']['buy_url'])
                except:
                    prodURL.append('')
                try:
                    prodImg.append(result['item']['enrichment']['images']['primary_image_url'])
                except:
                    prodImg.append('')
                try:
                    imgKey = _dIMG(result['item']['enrichment']['images']['primary_image_url'], 'product_images_Target', temp_prod_title)
                    prodImgPath.append(imgKey)
                except Exception as e:
                    prodImgPath.append('')

        totalProducts = []
        for i in range(len(price)):
            try:
                totalProducts.append((product_title[i], price[i], prodURL[i], prodImg[i], prodImgPath[i]))
                _sp(prodURL[i], product_title[i], price[i].replace('$', '').replace(',', ''), prodKW, prodRetailer, prodImgPath[i])
            except Exception as e:
                pass

        print('TARGET \n--------------------------------------------------------')
        try:
            for i in range(cap):
                print(totalProducts[i])
                print()
        except Exception as e:
            print(e)
            print('sec 2')

        finally:
            #_cl(prodImgPath, cap, 'product_images_Target')
            #return prodImgPath
            #return len(totalProducts)
            return results_json
            
    
if __name__ == '__main__':
    x = scrapeDataTarget('https://www.target.com/s?searchTerm=watch', 'testKW', 1)
    #x = scrapeDataNewegg('https://www.newegg.com/p/pl?N=100093102%20600480562', 1, 'tt')
    #x = scrapeDataAMZ('https://www.amazon.com/s?k=memory&crid=23J6NKRBFNT14&sprefix=%2Caps%2C68&ref=nb_sb_noss', 1, 'testKW')
    #x = refreshTokens('https://www.target.com/s?searchTerm=tv')
    #x = scrapeDataAMZ('https://www.amazon.com/s?k=table&crid=3O51A4P7GR9TN&sprefix=table%2Caps%2C137&ref=nb_sb_noss_1', 1, 'testKW')

    
