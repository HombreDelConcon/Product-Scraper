import mysql.connector
import time

def _store_product_info(url, prod_name, prod_price, kw, retailer, image_path):
    db = mysql.connector.connect(
        host='127.0.0.1',
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

def _scraper_Logs(scraper_instance, date, time, function_name, log_type, log_description):
    db = mysql.connector.connect(
        host='127.0.0.1',
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
    
def _clear_Table(table_name=None):
    db = mysql.connector.connect(
        host='127.0.0.1',
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

def _instantiate():
    db = mysql.connector.connect(
        host='127.0.0.1',
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

def _is_in_db(keyword):
    db = mysql.connector.connect(
        host='127.0.0.1',
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

def _get_info_by_kw(keyword):
    if _is_in_db(str(keyword)):
        db = mysql.connector.connect(
            host='127.0.0.1',
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

def _storeBlob(filepath, prodName):
    db = mysql.connector.connect(
        host='127.0.0.1',
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

def _generate_img_key(productName):
    sp1 = str(time.monotonic()).replace('.', '')
    sp2 = str(productName).replace(' ', '').replace('.', '')
    key = sp2 + sp1
    return key

if __name__ == '__main__':
    #x = _scraper_Logs(2, '2/3/4', '2:33', 'scrapah', 'error', 'scraper not working')
    x = _clear_Table('product_pictures')
    #x = _instantiate()
    #x = _is_in_db('Phone')
    #x = _get_info_by_kw('Phone')

