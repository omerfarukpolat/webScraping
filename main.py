import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import datetime
from progressbar import *
from IPython.display import clear_output
from urllib3.util import url

sections = ["https://www.dunyahalleri.com/category/haftanin-ozeti/page/",
            "https://www.dunyahalleri.com/category/genel-gundem/page/",
            "https://www.dunyahalleri.com/category/teknoloji-bilim/page/",
            "https://www.dunyahalleri.com/category/internet-girisimler/page/",
            "https://www.dunyahalleri.com/category/tasarim-inovasyon/page/",
            "https://www.dunyahalleri.com/category/kultur-sanat/page/"]

urls = []
# Öncelikle bir Kategori seçiyoruz.
for section in sections:
    # Kategorinin içerisinde sırayla 100 sayfa gezineceğiz.
    for i in range(1, 30):
        try:
            # Öncelikle URL'imizi oluşturuyoruz. Örneğin;
            # https://www.dunyahalleri.com/category/kultur-sanat/page/25
            newurl = section + str(i)
            print(newurl)

            # Url'nin içerisindeki bütün html dosyasını indiriyoruz.
            html = requests.get(newurl).text
            soup = bs(html, "xml")

            # Yukarıdaki şemadada görüldüğü gibi bütün makaleler bu  element'in içerisinde yer alıyor.
            # Bizde bütün makaleleri buradan tags adında bir değişkene topluyoruz.
            tags = soup.findAll("div", class_="row row-eq-height herald-posts")[0]

            # Sırayla bütün makalelere girip, href'in içerisindeki linki urls adlı listemize append ediyoruz.
            for a in tags.find_all('a', href=True):
                urls.append((section.split("/")[4], a['href']))
        except IndexError:
            break

urldata = pd.DataFrame(urls)
urldata.columns = ["Kategori", "Link"]
urldata.head()

urldata = urldata.drop_duplicates()
urldata.to_csv('urldata.csv')

html = requests.get(url).text
soup = bs(html, "lxml")
#Belirlediğimiz element'in altındaki bütün p'leri seçiyoruz.
body_text = soup.findAll("div", class_="tldr-post-content")[0].findAll('p')
#Body_text adındaki metni tek bir string üzerinde topluyoruz.
body_text_big = ""
for i in body_text:
    body_text_big = body_text_big +i.text

#Url içerisindeki html'i indiriyoruz.
html = requests.get(url).text
soup = bs(html, "lxml")
#Özetin bulunduğu element'in metin kısmını alıyoruz.
summarized = soup.find("div", class_="tldr-sumamry").text


#Url içerisindeki html'i indiriyoruz.
html = requests.get(url).text
soup = bs(html, "lxml")
#Başlığı ve zamanı'da element isimlerinden bu şekilde seçip, metinlerini alıyoruz.
header = soup.find("h1", class_="entry-title h1").text
timestamp = soup.find("span", class_="updated").text