from urllib.request import Request, urlopen, urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import time
from selenium.webdriver.common.keys import Keys

#SQL shit
db = mysql.connector.connect(host="localhost",user="root",password="Starcraft2")
cursor = db.cursor(buffered = True)
cursor.execute("use best_girl;")


#Selenium Shit
opts = webdriver.ChromeOptions()
opts.add_argument("user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 ")
driver = webdriver.Chrome(executable_path = "C:\\Users\\Caipo\\Desktop\\chromedriver.exe" , options = opts)


def open_images(name):
    global cursor, driver 

    cursor.execute("select * from links where name =  \"" +  name + "\" ;")
    data = [ [i[0], i[2]] for i in cursor]
    
    for i in data:
        print(i[1])
        driver.get(i[1])
        
        if input(name + " delete:") == "d":
            print( "Deleted" )
            cursor.execute("DELETE FROM links WHERE id =\"" + str(i[0]) + " \" ;")
            db.commit()
        
        
cursor.execute("select * from anime_girls;")
names = { i[0] : i[1::] for i in cursor}


for i in names :
    open_images(i)
