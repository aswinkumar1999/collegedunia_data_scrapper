This is an Python Script to Scrap Data from the Website `collegedunia.com` to create College Databases.

This is An Script i wrote to Save Time  , So the Accuracy is not great and manual inspection is necessary after the script completes it's task.

Here is a .csv scrapped for Chennai Colleges --> [Here](https://github.com/aswinkumar1999/collegedunia_data_scrapper/blob/master/colleges_chennai.csv)

# For Linux Users 

There are a list of dependencies to Install 

First of All , This is Tested in Linux ( Ubuntu 18.10 ) and should work with other Linux distros as well. 

To Run this you need to open a terminal and 

`sudo apt-get update && sudo apt-get install git python-pip`

`git clone https://github.com/aswinkumar1999/collegedunia_data_scrapper.git`


`pip install beautifulsoup4 requests selenium pandas`

`cd collegedunia_data_scrapper`


#### If Chrome Isn't Installed , then 

`sudo apt-get install libxss1 libappindicator1 libindicator7`

`wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`

`sudo apt install ./google-chrome*.deb`

You Also Need to Install Chrome Drivers, Follow the steps below 

1. Check your version of Google Chrome , Go to `https://www.whatismybrowser.com/` , It would Say the Version of Chrome as "Your Browser is Chrome 7x " , x = 3,4,5 

2. Go to `http://chromedriver.chromium.org/downloads` and Download the Version that you say above

3.Extract the Downloaded file and In Linux , Open an Terminal and type `sudo nautilus` and press enter , when prompted enter your password , Now , Copy the extracted file to `/usr/bin/` and paste it , After Pasting , Right Click - > Properties - Permission  and Check the box with "Allow Executing file as program" and make sure you see the check box ticked. You can close the tabs now.

Now , Open the web_scrapper.py in your favorite text editor.
Here change the `url = '......' `  to the url which you need to Scrap the lists of Data from , For this step you need to go to `collegedunia.com` and apply the selected location and type of College Filters and paste the Link in this..... 

After you edit the URL you can run the command by entering 

`python web_scrapper.py` to run the script.

After the Script exists , you can see a file named as `colleges.csv` , This file now contains all the details you need.

This Will take some time to scrap , I tested it on an 100Mbit Fiber connection with an Core i7 , so it took me ~10 minutes to get Details of 417 Colleges in Chennai ( Name , Address , Phone Number, Email ID and Weblink ) and put it in this [CSV file](https://github.com/aswinkumar1999/collegedunia_data_scrapper/blob/master/colleges_chennai.csv).

# For Windows Users

Install Anaconda based on your Computer Specs 

https://www.anaconda.com/distribution/#download-section 

Post Installation  

Search and Open Anaconda Navigator 

Once Anaconda Navigator is Opened , Click on Environments - > base (root) 

In the Top Drop down Box , Change from Installed to All 

Now Search for the following and make sure , it is checked for these names



beautifulsoup4

selenium

requests

pandas 

If any of them is Unchecked , Check them and Click Apply in the bottom right corner. Now these packages will get Installed.
After that you can close Anaconda Navigator 

After Installation You need to Install Chrome Driver :

Check your version of Google Chrome , Go to https://www.whatismybrowser.com/ , It would Say the Version of Chrome as "Your Browser is Chrome 7x " , x = 3,4,5

Go to http://chromedriver.chromium.org/downloads and Download the Version that you saw above.

and select Windows , Once it downloads extract the file "chromedriver.exe" to C:\Windows , ONLY THE FILE chromedriver.exe and not the Folder.

Now Download the Folder from Github and extract it to the desired Location and to Run the Script 

Press Shift+Right Click and Click on " Open Powershell Window here"  , Once the powershell Window opens , You need to enter 


`python .\web_scrapper.py`


and press Enter , It will create a File in Desktop with the Required Details 
