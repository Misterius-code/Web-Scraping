from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
import chromedriver_binary
from time import sleep
import pandas as pd
from PyPDF2 import PdfReader
from io import BytesIO
import openpyxl
from selenium.webdriver.common.by import By

def download_pdf():
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\Quake\AppData\Local\Google\Chrome\User Data\ ')
    PATH = r"C:\Users\Quake\Desktop\Artykuly\venv\Lib\site-packages\chromedriver_binary\chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=options)
    last_magazine=pd.read_csv("Gazeta.csv")['magazine_nr'].tail(1).iloc[0]

    url = str(input("Podaj link:"))
    while True:
        requests.get(url)
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        next_page = soup.find("li", class_="pager-next")
        print("PAGE: ",soup.find("li",class_="pager-current").text)
        articles = soup.find_all(class_='post-title')
        mg=1
        for article in articles:
            articles_list = []
            print("Magazine: ",mg,"/27")
            start_of_link = str(article).find('href="') + len('href="')
            end_of_link = str(article).find('"', start_of_link)
            # print("https://gpcodziennie.pl"+str(article)[start_of_link:end_of_link])
            # article_link= .get("https://gpcodziennie.pl"+str(article)[start_of_link:end_of_link])
            driver.get("https://gpcodziennie.pl" + str(article)[start_of_link:end_of_link])
            magazine_nr = driver.title[6:11]
            if int(magazine_nr) < int(last_magazine):
                soup = BeautifulSoup(driver.page_source, "html.parser")
                date = driver.title[13:23]
                source = driver.title[26:]
                if date.find("2014") == True:
                    driver.quit()
                    return
                i = 1
                nr_of_articles=len(soup.find_all('div', class_='clearfix post-block'))
                for pdf in soup.find_all('div', class_='clearfix post-block'):
                    print("Nr article ", i,"/",nr_of_articles)
                    article_title = pdf.find('h2', class_="post-title")
                    img = pdf.find('img')['srcset']
                    link = "https://gpcodziennie.pl" + article_title.a.get('href')
                    title = article_title.text
                    a_list = []
                    dzial = "NONE"
                    author = "NONE"
                    for a in pdf.find('div', class_='post-autor'):
                        a_list.append(a.text)
                    try:
                        if a_list[0] == "Autor: ":
                            author = a_list[1]
                        # list contian br
                        if a_list[3] == "Dział: ":
                            dzial = a_list[4]
                    except IndexError:
                        if a_list[0] == "Dział: ":
                            dzial = a_list[1]

                    driver.get(str(link))
                    # title=driver.title.replace(" | Gazeta Polska Codziennie","")
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # author = soup.find('div', class_="caption")
                    text = soup.find('div', class_='field-items').text.replace(
                        "Rozpocznij od początkuPrzewiń do tyłu o 10 sekundWstrzymajOdtwarzajPrzewiń do przodu o 10 sekundWłącz dźwiękWycisz",
                        "")

                    articles_list.append([title, magazine_nr, text, link, source, author, dzial, img, date])
                    i +=1
                excel(articles_list)
            mg+=1


        url="https://gpcodziennie.pl"+next_page.a.get('href')

    driver.quit()


def excel(article):
    print("EXCEL ACTIVATION")
    id=[]
    last_id=int(pd.read_csv("Gazeta.csv")['id'].tail(1).iloc[0])+1
    for i in range(last_id, last_id + len(article)):
        id.append(i)

    df = pd.DataFrame(article,index=id,
                    columns=['title', 'magazine_nr', 'text', 'link', 'source', 'author', 'department', "imgage", 'date'])
    df.to_csv('Gazeta.csv',mode='a', index=True ,header=False)
#pd.read_csv("Gazeta.csv")['id'].tail(1).iloc[0]

if __name__ == '__main__':
    download_pdf()
    # excel()
