urls = []
urls.append("https://collegedunia.com/science/visakhapatnam-colleges")
urls.append("https://collegedunia.com/education/visakhapatnam-colleges")
state = "Andhra Pradesh"

no_of_pagedowns = 100

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd

for u in urls:
    save_name = u[25:]+'.csv'
    save_name = save_name.replace("/","-")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(u)
    time.sleep(1)
    elem = browser.find_element_by_tag_name("body")
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.4)
        no_of_pagedowns-=1

    df = pd.DataFrame(columns=['S No','College Name', 'Address','State','Contact No(s)','E-Mail ID','Weblink'])

    html = browser.page_source
    main_page_content = BeautifulSoup(html,features="lxml")
    browser.close()
    Content = []
    for i in range(len(main_page_content.find_all("div", {"class": "clg-name-address"}))):
        paragraphs = main_page_content.find_all("div", {"class": "clg-name-address"})[i]
        link=url= paragraphs.a['href']
        name = paragraphs.text
        Content.append(paragraphs.text)
        link = url
        response = requests.get(link, timeout=10)
        page_content = BeautifulSoup(response.content, "html.parser")
        textContent = []
        for k in range(len(page_content.find_all("div",{"class": "address row"}))):
            paragraphs_new = page_content.find_all("div",{"class": "address row"})[k].text
            textContent.append(paragraphs_new)
        for l in range(len(textContent)):
            start = textContent[l].find('India')
            start_weblink = textContent[l].find('http')
            rev = textContent[l][::-1]
            rev_start = rev.find('mK')
            start_Ph = len(rev)-rev_start
            if(rev_start==-1):
                start_Ph = start+5
            http_val = textContent[l].find('http')
            end_Ph = textContent[l].find('GET')
            if(end_Ph==-1):
                end_Ph = http_val
            phone=textContent[l][start_Ph:end_Ph]
            j=0
            if(start>=0):
                address = textContent[l][0:start+5]
                weblink = textContent[l][start_weblink:]
                while(address.find("\n")>0):
                    loc = address.find("\n")
                    address = address.replace('\n',',')
            while(not phone[j].isdigit() and j < len(phone)-1):
                start_Ph=start_Ph+1
                j=j+1
            phone=textContent[l][start_Ph:end_Ph]
            phone = phone.replace(' ',',')
            while(phone.find(',,')>=0):
                phone = phone.replace(',,',',')
            if(phone[-1]==','):
                phone = phone[:-1]
        address=address.replace(',    ',',')
        textContent = []
        for o in range(len(page_content.find_all("script",{"type": "application/ld+json"}))):
            paragraphs = page_content.find_all("script",{"type": "application/ld+json"})[o].text
            textContent.append(paragraphs)
        for p in range(len(textContent)):
            start = textContent[p].find('email')
            if(start>=0):
                val=3
                end = '"'
                for j in range(100):
                    if (textContent[p][start+j] == end and val):
                        val=val-1
                        if(val==0):
                            end = j
                            email = textContent[p][start+8:start+end]
        print(name)
        list=[]
        list.append(i+1)
        list.append(name)
        list.append(address)
        list.append(state)
        list.append(phone)
        list.append(email)
        list.append(weblink)
        df.loc[i+1]=list
        df.to_csv(r'~/Desktop/'+save_name,index=None)
