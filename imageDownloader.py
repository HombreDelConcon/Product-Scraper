import requests
from bs4 import BeautifulSoup
import os
from os import listdir
from PIL import Image
import time
import mysql.connector
from db_Interactions import _store_product_info as _sP
from db_Interactions import _storeBlob


#Takes an image URL as a parameter as well as a folder name and stores the image as a JPG
#   in the specified directory
def _downloadImg(image_url:str , folder:str, productName:str) -> str:
    #Variable to store current working directory
    dir_arr = os.getcwd().split('\\')
    cur_dir = dir_arr[len(dir_arr)-1]
    #Check if the current directory is the target folder. If it isn't, then we attempt
    #   to create a folder within our current working directory, if the directory already
    #   exists then we move to that directory.
    if cur_dir != folder:
        try:
            os.mkdir(os.path.join(os.getcwd(), folder))
        except:     
            os.chdir(os.path.join(os.getcwd(), folder))
    dir_arr = os.getcwd().split('\\')
    dirAlreadyExists = dir_arr[len(dir_arr)-1] == folder

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7", "Upgrade-Insecure-Requests": "1", "X-Amzn-Trace-Id": "Root=1-62a166a2-296fb82b3224ff4735f4f091"}#6292aed6-1f65c2db636f27cb7ebcb533"}

    #makes the path to the image
    image_name = str(image_url).replace(' ', '_').replace(':', '__').replace('/', '')

    #Check if the image is in .jpg format already, if it isen't then it makes it into a .jpg
    if image_name[len(image_name)-4:] != '.jpg':
        image_name = image_name + '.jpg'
    path = None

    #Temporary variable to store current image path in case condtitons are not met
    temp = os.getcwd() + '\\' + image_name

    #Store the product Key to reference the picture in the product_images table
    pKey = None
    
    #If the image does not already exist then it creates a new image and stores it in the
    #   directory
    with open(image_name, 'wb') as f:
        im = requests.get(image_url)
        f.write(im.content)
        path = os.getcwd() + '\\' + image_name
    pKey = _storeBlob(image_name, productName)
    os.chdir('..')
    return pKey


#Deprecated function to clean directories of images. You pass in a list, a maximum number
#   images that you want to keep, and the folder name. It will go ahead and delete any images
#   that are above the cap, e.g. if I pass in a list of image paths and a cap of 20 with a
#   folder name of img_folder, it will store the first 20 images in the list of images and
#   delete every other image that is not within the 20 specified in the img_folder directory
def _clean_remainder(img_list:list , cap:int, folder:int) -> None:
    DeprecationWarning('This function is deprecated and is not necessary')
    cur_dir = os.getcwd().split('\\')
    cur_dir = cur_dir[len(cur_dir)-1]

    if cur_dir != folder:
        try:
            os.chdir(os.path.join(os.getcwd(), folder))
        except:
            raise BaseException('Directory does not exist')
    
    sliced_list = img_list[cap:]
    for image_path in sliced_list:
        if os.path.isfile(image_path):
            os.remove(image_path)

#Retrive images from the database and returns them as a BLOB 
def _retrieveBlob(blobID:str) -> bytes:
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='hoslyDB',
        password='Extr@ctoso700',
        database='scraperp1'
    )
    cursor = db.cursor()
    SQL = 'call P1getImage(%s)'
    VAL = (blobID, )
    cursor.execute(SQL, VAL)
    result = cursor.fetchone()[1]
    return result

#Resize desired image that is fed to it. It stores the images in a 
#   specific path since this function was not really mean to aid the 
#   scraper directly.
def _img_resize(img_path:str , imageWidth:int, imageHeight:int) -> bytes:
    image = Image.open(img_path)
    new_img = image.resize((imageWidth, imageHeight))
    new_img.save('shots\\TargetLogoResizedPy.png')
    print(new_img.size)
    return new_img
        
def main():
    #x = _downloadImg('https://c1.neweggimages.com/ProductImageCompressAll300/A0SD_1_20190708301467451.jpg', 'product_images_Newegg', 'Random Name')
    #x = _img_resize('shots\\TargetLogo.png', 90, 115)
    #x = _retrieveBlob('RandomName182075969')
    x = 1
    return x
if __name__ == '__main__':
    x = main()
