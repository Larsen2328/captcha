import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


#Chargement du driver chrome pour Selenium
driver = webdriver.Chrome(ChromeDriverManager().install())

#Obtention de l'url
driver.get("http://127.0.0.1:5500/index.html")

#Temps de pause (lié au JS pour l'affichage du code)
time.sleep(1)

#On trouve l'élément HTML de l'image grâce à son id
imageCaptcha = driver.find_element_by_id('image')
#On récupère l'uri de la source de l'image
srcImage = imageCaptcha.get_attribute('src')

#On stocke l'image récupérée à la racine du projet
urllib.request.urlretrieve(srcImage, "captcha.png")
#On "ouvre" cette image afin de la traiter
image = Image.open("captcha.png")
#On applique un filtre dessus
image = image.filter(ImageFilter.MedianFilter())
#On essaie d'améliorer le contraste
enhancer = ImageEnhance.Contrast(image)
#On applique un coefficient pour améliorer l'image/ 1=image identique / + = plus de contraste, brillance, ...
image = enhancer.enhance(4)
#On convertit l'image en noir et blanc
image = image.convert('1')
#on peut afficher l'image traitée
#image.show()

#On charge Tesseract. A télécharger au préalable. Tout est indiqué dans le Github du projet https://github.com/tesseract-ocr/tesseract#installing-tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#On stocke la "lecture" faite par Tesseract
reponse = pytesseract.image_to_string(image)
#On l'affiche en console
print(reponse)

#On capte le champ de saisie de la réponse avec son name
inputReponse = driver.find_element_by_name('reponse')
#On vide le champ (par précaution)
inputReponse.clear()
#On copie le code obtenu
inputReponse.send_keys(reponse)

#On cherche le bouton de validation. Recherche plus complexe à partir de la balise HTML et de son type
valider = driver.find_element_by_xpath('//input[@type="button"]')
#On simule un clic
valider.send_keys(Keys.ENTER)

