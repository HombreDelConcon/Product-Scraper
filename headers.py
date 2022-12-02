import string
from bs4 import BeautifulSoup as bs
import requests
import re

def _scrapeHeaders() -> str:
    url = "http://httpbin.org/get"
    site = requests.get(url)
    rawHTML = site.text

    soup1 = bs(rawHTML, 'lxml')
    soup2 = bs(soup1.prettify(), 'lxml')

    headers = soup2.find('p')
    string = headers.text

    return string

def _getAcceptEncoding(html:str) -> str:
    try:
        acceptEncodingPattern = re.compile(r'("Accept-Encoding"): (".+")')
        matches = acceptEncodingPattern.search(html)

    except AttributeError:
        print('No matches for Accept Encoding')
    else:
        return (matches.group(1), matches.group(2))

def _getAccept(html:str) -> str:
    try:
        AcceptPattern = re.compile(r'("Accept"): (".+")')
        matches = AcceptPattern.search(html)

    except AttributeError:
        print('THere are no matches for Accept')
    else:
        return (matches.group(1), matches.group(2))

def _getHost(html:str) -> str:
    try:
        HostPattern = re.compile(r'("Host"): (".+")')
        matches = HostPattern.search(html)
    except:
        print('There are not matches')
    else:
        return (matches.group(1), matches.group(2))

def _getUserAgent(html:str) -> str:
    try:
        UserAgentPattern = re.compile(r'("User-Agent"): (".+")')
        matches = UserAgentPattern.search(html)
    except:
        print('There are no matches')
    else:
        return (matches.group(1), matches.group(2))
def _getAmzTrace(html:str) -> str:
    try:
        amzTracePattern = re.compile(r'("X-Amzn-Trace-Id"): (".+")')
        matches = amzTracePattern.search(html)
    except:
        print('No matches found')
    else:
        return (matches.group(1), matches.group(2))

def headerDict() -> dict:
    stringHTML = _scrapeHeaders()

    AE = _getAcceptEncoding(stringHTML)
    A = _getAccept(stringHTML)
    H = _getHost(stringHTML)
    UA = _getUserAgent(stringHTML)
    AT = _getAmzTrace(stringHTML)

    arrayOfHeaders = [AE, A, H, UA, AT]
    finalDict = {}

    for header in arrayOfHeaders:
        finalDict.update({header[0]:header[1]})
    
    return finalDict
    
    #for key,value in finalDict.items():
    #    print('%s : %s' % (key, value))

    
if __name__ == '__main__':
    headerDict()
