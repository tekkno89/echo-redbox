from bs4 import BeautifulSoup
from selenium import webdriver
import re, time, signal

driver = webdriver.PhantomJS()
driver.implicitly_wait(2)

def getBoxes(zipcode='78759'):
   # This function is to get all boxes to store data
   boxesDictionary = {}
   getBoxQuery = 'http://www.redbox.com/locations?loc={}'.format(zipcode)
   reBoxList = re.compile('kiosk')

   driver.get(getBoxQuery)
   boxResults = BeautifulSoup(driver.page_source, "html.parser")
   boxListResults = boxResults.find_all('li', {'class' : reBoxList})

   for val, li in enumerate(boxListResults):
      linkResult = li.find('a')
      kioskId = linkResult.get('kioskid')
      vendorName = li.find('span', { 'class' : 'storeresults-vendor'}).text.lstrip()
      vendorLocation = li.find('div', { 'class' : 'storeresults-details'})
      vendorStreet = vendorLocation.contents[0].lstrip()
      vendorCSZ = vendorLocation.contents[1].contents[0].lstrip()
#      print(vendorName)
#      print(vendorStreet)
#      print(vendorCSZ)
#      print(kioskId)
#      print('')

      boxesDictionary[val] = {'kioskId':kioskId, 'vendorName':vendorName, 'vendorStreet':vendorStreet, 'vendorCSZ':vendorCSZ}

#   for key, val in boxesDictionary.items():
#      print(key,val)

#   print(boxesDictionary[0]['vendorName'])

   return boxesDictionary

def getBoxMovies(zipcode='78759', kioskId='0'):
   # This function is to select box and return list of all movies

   moviesDictionary = {}

   if kioskId == '0':
      boxes = getBoxes(zipcode)

      for boxKey, boxValue in boxes.items():
         print('---', boxKey, '---')
         print(boxValue['vendorName'])
         print(boxValue['vendorStreet'])
         print(boxValue['vendorCSZ'])
         print('')

      kioskSelect = input('Select Number for Box Listed Above ')
      kioskId = boxes[int(kioskSelect)]['kioskId']
      print('You Selected Kiosk', kioskId)
   else:
      pass

driver.service.process.send_signal(signal.SIGTERM)
driver.quit()
