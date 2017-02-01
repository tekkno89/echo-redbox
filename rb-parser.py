from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re, time, signal

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"
)

driver = webdriver.PhantomJS(desired_capabilities=dcap)
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
      boxesDictionary[val] = {'kioskId':kioskId, 'vendorName':vendorName, 'vendorStreet':vendorStreet, 'vendorCSZ':vendorCSZ}

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

   getBoxQuery = 'http://www.redbox.com/locations?loc={}'.format(zipcode)

   driver.get(getBoxQuery)
   driver.find_element_by_id(kioskId).click()
   time.sleep(.5)
   driver.find_element_by_partial_link_text('See More').click()
   time.sleep(.5)
   page = BeautifulSoup(driver.page_source, "html.parser")

   find_newRelease = page.find('div', id="productlistrollupphysical3_ProductListOdopod_Widget")

   for i in find_newRelease.find_all('a'):
      print(i.text)

driver.service.process.send_signal(signal.SIGTERM)
driver.quit()
