from urllib.request import Request, urlopen, urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import time
from selenium.webdriver.common.keys import Keys
from google_images_search import GoogleImagesSearch
from os import getcwd

# SQL SHIT
db = mysql.connector.connect(host="192.168.1.122", user="caipo", password="password")
cursor = db.cursor(buffered=True)
cursor.execute("use bestgirl;")
cursor.execute("select * from anime_girls;")
data = {i[0]: i[1::] for i in cursor}

# Google
gis = GoogleImagesSearch('AIzaSyDYsTUHG8QLouIXt-ukVJFnkcAPZxzwobA', '2e34f29787dead3b7')

# Selnium set up for tennor
opts = webdriver.FirefoxOptions()
opts.add_argument(
    "user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 ")
driver = webdriver.Firefox(executable_path= getcwd() + "/geckodriver", options=opts)

def main():

    test = False
    contenders = [
        {"name": "Sinon", "series": "Sword Art Online", "plot": "small", "google": False, "tennor": True},
        {"name": "Faye", "series": "Cowboy Bebop", "plot": "Large", "google": False, "tennor": True},
        {"name": "Edward", "series": "Cowboy Bebop", "plot": "DFC", "google": False, "tennor": True}
    ]

    for contend in contenders:

        try:
            add_user(contend, test)
        except:
            print(f"already added")

        if contend["tennor"]:
            tennor_scrape(contend["name"], test)

        if contend["google"]:
            google_scrape(contend["name"], test)

def add_user(contender, test):
    global db, cursor

    cursor.execute( f'''insert into anime_girls ( contender_name, series, elo, number_matches, number_wins, plot)
                    values( \"{contender["name"]}\", \"{contender["series"]}\", 1000, 0, 0, \"{contender["plot"]}\"); 
                     '''
                  )
    if not test:
        db.commit()


def tennor_scrape(name, test=False):
    global driver, data, cursor, db
    cursor.execute("select * from anime_girls;")
    data = {i[0]: i[1::] for i in cursor}

    driver.get('https://tenor.com/')

    driver.find_element(by="name", value="q").send_keys(str(name) + " " + str(data[name][0]))
    driver.find_element(by="class name", value="iconfont-search").click()

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 500)")

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    gif_boxes = soup.find_all("a", activeclassname="current")
    href = "href"

    links = list()
    for i in gif_boxes:

        if "view" in i["href"] and "Sticker" not in str(i):

            driver.get(f"https://tenor.com{i[href]}")
            links.append(
                BeautifulSoup(driver.page_source, features="html.parser").find("div", class_="Gif").find("img")["src"]
                        )

    if not test:
        for i in links:
            cursor.execute(f"insert into links (name, link)  values(\"{name}\", \"{i}\");")
            db.commit()


    



def google_scrape(name, test):
    global cursor, db, data

    cursor.execute("select * from anime_girls;")
    data = {i[0]: i[1::] for i in cursor}

    print(name)
    li = list()

    _search_params = {
        'q': name + " " + data[name][0],
        'num': 10
    }

    gis.search(search_params=_search_params)
    for i in range(3):
        for i in gis.results():
            li.append(i.url)

        time.sleep(1)

        for url in li:
            print(url)
            try:
                cursor.execute(f'''insert into links(name, link) value( \"{name}\", \"{url}\");''')
            except:
                pass
    gis.next_page()
    if not test:
        db.commit()


if __name__ == "__main__":
    main()
