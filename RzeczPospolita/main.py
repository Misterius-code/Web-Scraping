from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
#import chromedriver_binary
#from time import sleep
import pandas as pd
#from PyPDF2 import PdfReader
#from io import BytesIO
#import openpyxl

from selenium.webdriver.common.by import By


def download_pdf():
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\Quake\AppData\Local\Google\Chrome\User Data\Profile 1\ ')
    PATH = r"C:\Users\Quake\Desktop\Artykuly\venv\Lib\site-packages\chromedriver_binary\chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=options)
    #last_magazine=pd.read_csv("rp.csv")['magazine_nr'].tail(1).iloc[0]
    #url = str(input("Podaj link:"))
    url="https://archiwum.rp.pl/2021/05/20"
    source = "Rzeczpospolita"
    last_magazine=pd.read_csv("Rzeczpospolita.csv")['magazine_nr'].tail(1).iloc[0]

    input()
    while True:

        requests.get(url)
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        date=url[-10:]
        no_publication_today=soup.find(class_="noPublicationToday")
        url = "http://archiwum.rp.pl" + soup.find("a", class_="pageListDateScrollRight")['href']

        if no_publication_today == None:

            print("DATE",date)
            magazine_nr=soup.find(id="issueNumber").text.replace("Wydanie:","").replace(" ","")

            if int(magazine_nr) > int(last_magazine):

                articles = soup.find_all(class_='pages')
                mg=1
                articles_list = []
                for article in articles:


                    print("Magazine: ", mg, "/", len(articles))
                    link_article=article.find_all('a',href=True)
                    for link_to_article in link_article:

                        link="https://archiwum.rp.pl"+link_to_article['href']

                        driver.get(link)
                        #test=requests.get("https://archiwum.rp.pl"+link['href'])

                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        try:
                            artDetails=soup.find(class_="artDetails").text
                        except AttributeError:
                            break
                            #="Unknow | Unknow | Unknow"
                        try:
                            autor_descp = soup.find(class_="seealso").text
                        except AttributeError:
                            autor_descp=""
                        print(autor_descp.replace('\n',""))
                        artDetails=artDetails.split('|')
                        author="None"
                        dzial="None"
                        if len(artDetails)==3:
                            author=artDetails[2]
                        dzial = artDetails[1]

                        img=soup.find(class_='fot')
                        image_text="None"
                        if img != None:
                            image_text = img.text.replace('\n',"")

                            img=img.find('a',href=True)['href']

                        else:
                            img="None"

                        title = soup.find(class_="articleTitle").text
                        text=soup.find(class_="storyContent").text.replace('\n',"")


                        #text=text.replace(image_text,"")
                        text=text.replace(autor_descp.replace('\n',""),"")
                        print(text)


                        articles_list.append([title, magazine_nr, text, link, source, author, dzial, img,image_text, date])
                    mg += 1

                excel(articles_list)








    driver.quit()


def excel(article):
    print("EXCEL ACTIVATION")
    id=[]
    last_id=int(pd.read_csv("Rzeczpospolita.csv")['id'].tail(1).iloc[0])+1

    for i in range(last_id, last_id + len(article)):
        id.append(i)

    df = pd.DataFrame(article,index=id,
                    columns=['title', 'magazine_nr', 'text', 'link', 'source', 'author', 'department', "imgage",'image_text', 'date'])
    df.to_csv('Rzeczpospolita.csv',mode='a', index=True ,header=False)
    return
#pd.read_csv("Gazeta.csv")['id'].tail(1).iloc[0]

if __name__ == '__main__':
    download_pdf()
    # excel()
