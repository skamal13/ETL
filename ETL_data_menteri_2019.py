# @autor: Syamsul Kamal
# @github: github.com/skamal13


from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import psycopg2 

# URl to web scrap from.
# in this example we web scrap Kabinet Indonesia Maju from id.wikipedia.org
page_url = "https://id.wikipedia.org/wiki/Kabinet_Indonesia_Maju"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
page_soup = soup(uClient.read(), "html.parser")
uClient.close()


#create connection to the database
con = psycopg2.connect(database="belajar", user="xxxx", password="xxxx", host="127.0.0.1", port="5432")
#create a cursor object
cur = con.cursor()


# finds data from the page_soup
tables = page_soup.find_all('table',{"class": "wikitable"})
tr = tables[1].find_all('tr')

i=2
# loops over each table and grabs the data
while i<len(tr):
    td = tr[i].find_all('td')
    if len(td)!=0 and len(td)!=6:
        #INSERT statement via the execute() method to add the data into the table
        cur.execute("INSERT INTO menteri2019 (jabatan,nama,url,mulai_menjabat,selesai_menjabat,partai) \
            VALUES (%s,%s,%s,%s,%s,%s)",\
                (td[1].get_text(strip=True),td[3].get_text(strip=True),td[3].select('a')[0].get('href'),td[4].get_text(strip=True),td[5].get_text(strip=True),td[7].get_text(strip=True)))
        con.commit()
    i+=1
# Close the database
con.close()

#---End of code---
