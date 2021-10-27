import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


import pytesseract
from PIL import Image, ImageEnhance, ImageFilter



driver = webdriver.Chrome(ChromeDriverManager().install())


driver.get("http://127.0.0.1:5500/index.html")

time.sleep(1)

imageCaptcha = driver.find_element_by_id('image')
srcImage = imageCaptcha.get_attribute('src')

urllib.request.urlretrieve(srcImage, "captcha.png")
image = Image.open("captcha.png")

image = image.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(4)
image = image.convert('1')
#image.show()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
reponse = pytesseract.image_to_string(image)
print(reponse)

inputReponse = driver.find_element_by_name('reponse')
inputReponse.clear()
inputReponse.send_keys(reponse)

valider = driver.find_element_by_xpath('//input[@type="button"]')
valider.send_keys(Keys.ENTER)

