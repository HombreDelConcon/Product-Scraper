import mysql.connector
import time

#Updated: 12/02/22

#Designed to store all the functions used to interact with the database which I am still trying to figure out how not
#   to run on a localhost

#Store product information in the database about the products
def _store_product_info(url: str, prod_name:str, prod_price: float, kw: str, retailer: str, image_path: str) -> None:
    db = mysql.connector.connect(
        host='24.102.174.6',
        user='hoslyDB',
        password='Extr@ctoso700',
        database='scraperp1'
    )
    cursor = db.cursor()

    SQL = "call P1insertInfo(%s, %s, %s, %s, %s, %s)"
    VAL = (url, prod_name, prod_price, kw, retailer, image_path)
    cursor.execute(SQL, VAL)
    db.commit()
    #print(cursor.rowcount, 'record inserted')

#Log information about the running processes to the database
def _scraper_Logs(scraper_instance: int, date: str, time: str, function_name: str, log_type: str, log_description: str) -> None:
    db = mysql.connector.connect(
        host='24.102.174.6',
        user='hoslyDB',
        password='Extr@ctoso700',
        database='scraperp1'
    )
    cursor = db.cursor()

    SQL = "call P1createLog(%s, %s, %s, %s, %s, %s)"
    VAL = (scraper_instance, date, time, function_name, log_type, log_description)
    cursor.execute(SQL, VAL)
    db.commit()
    #print(cursor.rowcount, 'record inserted')

#Clear specified database table/ truncate table
def _clear_Table(table_name: str=None) -> None:
    db = mysql.connector.connect(
        host='24.102.174.6',
        user='hoslyDB',
        password='Extr@ctoso700',
        database='scraperp1'
    )
    cursor = db.cursor()
    inp = table_name
    if table_name == None:
        inp = input('1: prodinformation \n2: scrapelogs \n')
        if inp == '1':
            inp = 'prodinformation'
        elif inp == '2':
            inp = 'scrapelogs'
        else:
            raise BaseException('No valid input provided')

    SQL = "truncate table %s"
    VAL = (inp,)
    format_val = SQL % VAL
    cursor.execute(format_val)
    db.commit()
    #print('Table %s cleared' % VAL)

#Keep track of the instance in which the web scraper is running for debugging purposes 
def _instantiate() -> int:
    db = mysql.connector.connect(
        host='24.102.174.6',
        user='hoslyDB',
        password='Extr@ctoso700',
        database='scraperp1'
    )
    cursor = db.cursor()
    SQL = 'select MAX(scraperInstance) from scrapelogs'
    cursor.execute(SQL)
    result = cursor.fetchall()
    scraperInstance = False

    if result[0][0] == None:
        scraperInstance = 1
    else:
        scraperInstance = int(result[0][0]) + 1
    return scraperInstance

#Check if a product is already in the database
def _is_in_db(keyword: str) -> bool:
    db = mysql.connector.connect(
        host='24.102.174.6',
        user='hoslyDB',
        password='Extr@ctoso700',
        database='scraperp1'
    )
    cursor = db.cursor()

    SQL = 'call P1getAllInfoByKW(%s)'
    VAL = (str(keyword),)
    cursor.execute(SQL, VAL)
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

#Search database for all instances of a keyword
def _get_info_by_kw(keyword: str) -> list:
    if _is_in_db(str(keyword)):
        db = mysql.connector.connect(
            host='24.102.174.6',
            user='hoslyDB',
            password='Extr@ctoso700',
            database='scraperp1'
        )
        cursor = db.cursor()

        SQL = 'call P1getAllInfoByKW(%s)'
        VAL = (str(keyword),)
        cursor.execute(SQL, VAL)
        result = cursor.fetchall()
        lenNewegg = 0
        lenAMZ = 0
        lenTarget = 0
        for item in result:
            print((item[1], item[2], item[0], item[3], item[4], item[5]))
            print()
            if item[4] == 'Target':
                lenTarget += 1
            elif item[4] == 'Amazon':
                lenAMZ += 1
            elif item[4] == 'Newegg':
                lenNewegg += 1
        return (lenNewegg, lenAMZ, lenTarget)    
    return None

#Store BLOBs in the database. Basically storing images in bytes and return a key to reference the image
def _storeBlob(filepath: str, prodName: str) -> str:
    db = mysql.connector.connect(
        host='24.102.174.6',
        user='hoslyDB',
        password='Extr@ctoso700',
        database='scraperp1'
    )
    cursor = db.cursor()
    binData = None
    with open(filepath, 'rb') as file:
        binData = file.read()
        
    SQL = 'call P1insertImage(%s, %s)'
    imgKey = _generate_img_key(prodName)
    VAL = (imgKey, binData)
    cursor.execute(SQL, VAL)
    db.commit()
    return imgKey

#Generate unique key for each image name that is fed to it
def _generate_img_key(productName: str) -> str:
    sp1 = str(time.monotonic()).replace('.', '')
    sp2 = str(productName).replace(' ', '').replace('.', '')
    key = sp2 + sp1
    return key

if __name__ == '__main__':
    #x = _scraper_Logs(2, '2/3/4', '2:33', 'scrapah', 'error', 'scraper not working')
    #x = _clear_Table('product_pictures')
    x = _instantiate()
    #x = _is_in_db('Phone')
    #x = _get_info_by_kw('Phone')
    print(x)

