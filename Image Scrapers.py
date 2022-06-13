from urllib.request import Request, urlopen, urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import time
from selenium.webdriver.common.keys import Keys
from google_images_search import GoogleImagesSearch



#SQL SHIT
db = mysql.connector.connect(host="localhost",user="root",password="Starcraft2")
cursor = db.cursor(buffered=True)
cursor.execute("use best_girl;")
cursor.execute("select * from anime_girls;")
data = { i[0] : i[1::] for i in cursor}

#Google 
gis = GoogleImagesSearch('AIzaSyDYsTUHG8QLouIXt-ukVJFnkcAPZxzwobA', '2e34f29787dead3b7')


#Selnium set up for tennor
opts = webdriver.ChromeOptions()
opts.add_argument("user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 ")
driver = webdriver.Chrome(executable_path = "C:\\Users\\Caipo\\Desktop\\chromedriver.exe" , options = opts)



def tennor_scrape(name, Test = False):
    global driver, data
    
    driver.get('https://tenor.com/')

    driver.find_element_by_name("q").send_keys( str(name) + " " + str(data[name][0]) )
    driver.find_element_by_class_name("iconfont-search").click()
     

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 3000)")
    
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, features="html.parser")


    li = list()
    for i in soup.find_all("div",  class_="Gif"):
        li.append(i.find("img")["src"])


    for url in li:
        print(url)

    
        cursor.execute(f'''insert into links(name, link)
    value( \"{name}\", \"{url}\");''')

    if not Test:
        db.commit()




def google_scrape(name):
    
    
    
    global cursor, db, data

    
    li = list()

        
        
    _search_params = {
        'q': name +" "+ data[name][0],
        'num': 10
        }


    gis.search(search_params=_search_params)

    for i in gis.results():
        li.append(i.url)

    time.sleep(1)

        
    for url in li:
        print(url)

        try:
            cursor.execute(f'''insert into links(name, link)
    value( \"{name}\", \"{url}\");''')
        except:
            print( "error" )
    print(len(li))

    if not Test:
        db.commit()


    
for i in data:
    tennor_scrape(i, Test = True)





