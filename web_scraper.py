#..........................................................................................
# Date : May 14 2019
# Author : Aswinkumar
# Summary : This Script first goes to the specified webpage to take the list of colleges
#           and it iteratively goes into every website and extracts the name , address ,
#           phone number , email id ( if available) , and weblink and puts it into a csv
#           file as an output
#..........................................................................................
#url is a list which contains all the urls to get lists of colleges from
urls = []
urls.append("https://collegedunia.com/education/visakhapatnam-colleges")
#state has to be explicitly specified to print in the csv file
state = "Andhra Pradesh"
#how many time chrome has to scrool down in the page to get the full list as the page is dynamicaly loaded
no_of_pagedowns = 100

#Extracting Data from Website
#BeautifulSoup to extract contents from the website.
#requests

#Scrolling through the page dynamically
#selenium for using the chrome webdriver
#time to wait for a while and scroll down the page
#### Also Needs Chrome Driver to be explicitely installed to work with dynamicaly scrolling down pages ###

#Pandas to export the stored dataframe as a csv

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd

for u in urls:  #iterates throught the list urls
    save_name = u[25:]+'.csv'       # specifies the name pandas has to store it as
    save_name = save_name.replace("/","-")      # replaces / with - as the file name in the case would be invalid
    options = webdriver.ChromeOptions()         # we need to run chrome in headless mode so options
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')    # specifies the window size of the chrome
    browser = webdriver.Chrome(chrome_options=options)  # Starts a browser with that specified options
    browser.get(u)                              # opens the browser with the url from the iterator
    time.sleep(1)                               # waits for the page to load
    elem = browser.find_element_by_tag_name("body")     # gets the body tag from the html under which content is present
    while no_of_pagedowns:                      # scrolls the pages to the numeber of times
        elem.send_keys(Keys.PAGE_DOWN)          # pressed the down key
        time.sleep(0.4)                         # waits for the page to load
        no_of_pagedowns-=1                      # reduce the number of pagedowns by 1
    #Initiate a Pandas DataFrame with the Specific Columns
    df = pd.DataFrame(columns=['S No','College Name', 'Address','State','Contact No(s)','E-Mail ID','Weblink'])
    html = browser.page_source              # gets the page source once it's loaded
    main_page_content = BeautifulSoup(html)     # extracts the features using bs4
    browser.close()                         # closes the broswer ( important !!)
    Content = []                            #Initialize an empty list
    # Iterate throught the no of list of colleges
    for i in range(len(main_page_content.find_all("div", {"class": "clg-name-address"}))):
        paragraphs = main_page_content.find_all("div", {"class": "clg-name-address"})[i]
        link=url= paragraphs.a['href']              #gets the url of the colleges
        name = paragraphs.text                      #gets the name of the college
        Content.append(paragraphs.text)             # Appends the name to the content list
        link = url                                  # ----------redundant---------
        response = requests.get(link, timeout=10)   # get to fetch the details inside the url
        page_content = BeautifulSoup(response.content, "html.parser")  # parses the data using bs4
        textContent = []                            #empty list and it has lots of important data
        # this has the important data we now extract from
        for k in range(len(page_content.find_all("div",{"class": "address row"}))):
            paragraphs_new = page_content.find_all("div",{"class": "address row"})[k].text
            textContent.append(paragraphs_new)
        #This is the part we start extracting Address , phone number and weblink
        # As All colleges are from India , Address is collected assuming India to be the last line and extracted as such
        # Phone number starts after the Distance to nearest landmarks is show
        # As the number of landmarks are not fixed so the last landmark is found
        #using the reverse of the String and again reversed to find the position of the last landmark
        #The Details after the landmark happen to be Phone number , but in some cases
        #there are no landmarks in such cases, we directly use the details after India
        #weblink usually starts with http and ends till the last line
        #so finding where is http and using that as a start and the end of the string
        #to be the last line we can find the url of the colleges
        #
        #The Phone number usually ends with GET EMAIL ADDRTESS OF THE COLLEGES
        #So we check if we have a get , if not , then we use the end to be starting of weblink
        #

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

        #This is bit tricky but this is how you get the email address of the college
        #this is contained in a different location and it is extracted separately.
        textContent = []
        for o in range(len(page_content.find_all("script",{"type": "application/ld+json"}))):
            paragraphs = page_content.find_all("script",{"type": "application/ld+json"})[o].text
            textContent.append(paragraphs)
        #This part has lots of garbage along with the along with the email id.
        #this is usually in the format
        #"email"="asdasd@ssdaf.com"
        #the start is set to start of word email+ 8 characters
        # the end is when we encounter third " as it is the format the website saves
        # We also assume the maximum length of email should be 100 which is good enough for practical purpose.
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
        #Prints the name of the colleges
        #Create a list to store the detais and finally dumps into there Pandas dataframe
        print(name)
        list=[]
        list.append(i+1)
        list.append(name)
        list.append(address)
        list.append(state)
        list.append(phone)
        list.append(email)
        list.append(weblink)
        #it dumps it here
        df.loc[i+1]=list
        #pandas dumps it to the specified csv file from here.
        df.to_csv(r'~/Desktop/'+save_name,index=None,encoding='utf-8')
