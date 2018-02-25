from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
import time
import os

import rethinkdb as r

cnx = r.connect(host='192.168.1.6', port=28015, db='pbScrap')
#cust = r.table('customers')
#cust = r.table('customers_c_jose')
catch = r.table('catch')

IMAGES_DIR = os.path.join(os.getcwd(),'screenshots')

try:
    os.mkdir(IMAGES_DIR)
except Exception as e:
    pass

def insert(data):
    global cust
    global cnx
    cust.insert(data).run(cnx)

def registerError(data):
    global cust
    global cnx
    catch.insert(data).run(cnx)

"""
cnx = pymongo.MongoClient()
db = cnx["selenium"]
global tbl
tbl = db["customers"]
"""

global driver
driver = webdriver.Firefox()
#driver = webdriver.Chrome()
#driver = webdriver.Opera()
driver.get("http://www.paginasblancas.com.pe/")
#driver.get("http://www.paginasblancas.com.pe/persona/s/jorge/callao/p-45")
#driver.get("http://www.paginasblancas.com.pe/persona/s/rosa/callao/p-28")


name = 'carlos'
nLocality = u'callao'
bot = {}

bot.update(dict(
    DEBUG=True,
    SECRET_KEY='apeponkopy!',
    DB_HOST='db',
    DB_PORT=28015,
    DB_NAME='pbScrap',
    TBL_NAME="{}{}".format('customer_', name)
))

def init_db():
    #conn = r.connect(host='localhost', port=28015)
    try:
        global cnx
        global bot
        global r
        #r.db_create(bot['DB_NAME']).run(conn)
        #r.db(bot['DB_NAME']).table_create(bot['TBL_NAME']).run(conn)
        r.db(bot['DB_NAME']).table_create(bot['TBL_NAME']).run(cnx)
        r.db(bot['DB_NAME']).table(bot['TBL_NAME']).index_create('created').run(cnx)
        print('Database setup completed. Now run the app without --setup.')
    except Exception as e:
        print('App table already exists. Run the app without --setup.')

init_db()

cust = r.table(bot['TBL_NAME'])
#https://rethinkdb.com/docs/changefeeds/ruby/
#-------------------------------------------------- BEGIN [for scroll] - (23-02-2018 - 16:58:10) {{
#--------------------------------------------------
# WebElement element = driver.findElement(By.id("my-id"));
# Actions actions = new Actions(driver);
# actions.moveToElement(element);
# actions.perform();
#
#
# WebElement element = driver.findElement(By.id("id_of_element"));
# ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(true);", element);
# Thread.sleep(500);
#--------------------------------------------------
#-------------------------------------------------- END   [for scroll] - (23-02-2018 - 16:58:10) }}

#-------------------------------------------------- BEGIN [search by address] - (22-02-2018 - 13:25:31) {{
#--------------------------------------------------
# driver.find_element_by_xpath("//a[@data-target='address']").click()
# driver.find_element_by_name("street").send_keys("carlos izaguirre")
# driver.find_element_by_name("streetNumber").send_keys("2")
# #driver.find_element_by_id("aLocality").send_keys(u"los olivos\ue007")
# driver.find_element_by_id("aLocality").send_keys(u"los olivos")
#driver.find_element_by_id("btnSrchAddress").click()
#--------------------------------------------------
#-------------------------------------------------- END   [search by address] - (22-02-2018 - 13:25:31) }}

#-------------------------------------------------- BEGIN [search by name] - (22-02-2018 - 13:25:54) {{
driver.find_element_by_xpath("//a[@data-target='name']").click()
#driver.find_element_by_name("name").send_keys("juan")
driver.find_element_by_name("name").send_keys(name)
#driver.find_element_by_name("streetNumber").send_keys("2")
#driver.find_element_by_id("aLocality").send_keys(u"los olivos\ue007")
driver.find_element_by_id("nLocality").send_keys(nLocality)
driver.find_element_by_id("btnSrchName").click()
#-------------------------------------------------- END   [search by name] - (22-02-2018 - 13:25:54) }}

#http://selenium-python.readthedocs.io/api.html#selenium.webdriver.remote.webdriver.WebDriver.current_url
#search.send_keys(u'\ue007')
#selenium.keyPress("id="","\\13");
#1\N{U+E007}2\N{U+E007}3
#1\n2\n3

#driver.find_element_by_xpath("//a[@data-target='address']") #name address phone ddni /(/*[@id]")
#pag = driver.find_elements_by_xpath("//ul[@class='m-results-pagination']")
#lis = driver.find_elements_by_css_selector("ul.m-results-pagination li")
#qPages = 1

#spanQ = driver.find_element_by_xpath(".//span[@class='m-header--count']").text
#totalQ = spanQ.split()[0]

#-------------------------------------------------- BEGIN [lxml support] - (23-02-2018 - 15:35:44) {{
from lxml import html

root = html.fromstring(driver.page_source)

spanQ = root.xpath('//span[@class="m-header--count"]/text()')
totalQ = spanQ[0].split()[0]
#-------------------------------------------------- END   [lxml support] - (23-02-2018 - 15:35:44) }}

_round = 0
existPages = True
itemIndex = 0
pageNumber = 0

def q():
    driver.close()

def insertCustomer(c):
    global tbl
    global totalQ
    global insert
    #tbl.insert_one({'name':c[0], 'address':c[2], 'city': c[4], 'phone': c[8], 'script': c})
    #tbl.insert_one({'name':c[0], 'address':c[1], 'city': c[2], 'phone': c[3], 'script': c[4]})
    #insert({'name':c[0], 'address':c[1], 'city': c[2], 'phone': c[3], 'script': c[4], 'epoch': c[5], 'ins': c[6], 'url': c[7], 'search': c[8], 'nLocality': c[9], 'pagePosition': c[10], 'itemIndex': c[11], 'totalQ': totalQ})
    insert(c)

def search():
    global driver
    global name
    global nLocality
    global itemIndex
    global pageNumber
    global IMAGES_DIR
    global html
    pageNumber += 1
    url = driver.current_url
    date = time.strftime("%Y-%m-%d")
    imageName = "{}-{}.{}".format(date, url[url.index('/',7)+1:].replace('/','-'), '.png')
    #imagePath = os.path.join(IMAGES_DIR,imageName)
    imagePath = "{}/{}".format(IMAGES_DIR,imageName)
    driver.get_screenshot_as_file(imagePath)
    pos = 0
    try:
        #items = driver.find_elements_by_css_selector("li.m-results-business")
        root = html.fromstring(driver.page_source)
        items = root.cssselect('li.m-results-business')

        time.sleep(2)
        lis = driver.find_elements_by_css_selector("ul.m-results-pagination li")
        #lisl = root.cssselect('ul.m-results-pagination li')
        qPages = len(lis)

        records = []
        for i in items:
            #scriptContent = i.find_element_by_tag_name("script").get_attribute("innerHTML")
            scriptContent = i.find("script").text
            #"""
            #s = i.find_element_by_tag_name("script")

            #nombre = i.find_element_by_css_selector("h3 a").text
            nombre = i.cssselect("h3 a")[0].text

            #direccion = i.find_element_by_xpath(".//span[@itemprop='streetAddress']").text
            direccion = i.xpath(".//span[@itemprop='streetAddress']/text()")[0].strip()

            #ciudad = i.find_element_by_xpath(".//span[@itemprop='addressLocality']").text
            ciudad = i.xpath(".//span[@itemprop='addressLocality']/text()")[0].strip()

            #telefono = i.find_element_by_css_selector("div.m-button--results-business--see-phone").get_attribute("onclick").split(",")[1].strip()[:-1]
            telefono = i.cssselect("div.m-button--results-business--see-phone")[0].attrib['onclick'].split(',')[1].strip()[:-1]

            #"""
            i = scriptContent.index("[")+1
            f = scriptContent.index("]")
            data = scriptContent[i:f].replace("'","").split(",")
            epoch = int(time.time())
            ins = time.strftime("%Y-%m-%d %H:%M:%S")
            pos += 1
            itemIndex += 1
            data = [nombre, direccion, ciudad, telefono, data, epoch, ins, url, name, nLocality, pos, itemIndex, pageNumber]
            #data = scriptContent[i:f].replace("'","").encode("iso8859-1","ignore").decode("iso8859-1").split(",")
            global totalQ
            records.append({'name':data[0], 'address':data[1], 'city': data[2], 'phone': data[3], 'script': data[4], 'epoch': data[5], 'ins': data[6], 'url': data[7], 'search': data[8], 'nLocality': data[9], 'pagePosition': data[10], 'itemIndex': data[11], 'totalQ': totalQ, 'pageNumber': pageNumber, 'image': imageName})
    except Exception as e:
        global registerError
        data = {'error': str(e), 'inURL': url, 'inItem': itemIndex, 'inPosition': pos, 'inPageNumber': pageNumber, 'image': 'under ...'}
        driver.refresh()
        search()
        registerError(data)
    global insertCustomer
    insertCustomer(records)
    print("qPages: %d \n" % qPages)
    lastPage = lis[qPages-1]
    #print("qPages: %d \n" % lastPage)
    global existPages
    if lastPage.get_attribute("class") != "is-active":
    #if lastPage.attrib["class"] != "is-active":
        try:
            lastPage.click()
        except Exception as e:
            driver.refresh()
            search()


    else:
        existPages = False

    print(existPages)
    #is-active
    #last



while existPages:
    if pageNumber > 90:
        time.sleep(10)
    search()
q()

#script = "return $(\"td:contains('{}')\").length".format(text="Silver")
#count = driver.execute_script(script)
#count =  driver.find_elements_by_xpath("//td[text()='Silver']")
#search_button = self.driver.find_element(By.XPATH, './/*[@id="nav-search"]/form/div[2]/div/input').click()
#var xpath = "a[text()='SearchingText']";
#var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
#var xpath = "a[contains(text(),'Searching')]";
