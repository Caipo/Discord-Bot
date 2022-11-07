from selenium import webdriver
import mysql.connector
from os import getcwd

#SQL shit


db = mysql.connector.connect(host="192.168.1.122",user="caipo",password="password")
cursor = db.cursor(buffered = True)
cursor.execute("use bestgirl;")

# Selnium set up for tennor
opts = webdriver.FirefoxOptions()
opts.add_argument(
"user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 ")
driver = webdriver.Firefox(executable_path= getcwd() + "/geckodriver", options=opts)

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
names = {"Llenn"}


for i in names :
    open_images(i)
