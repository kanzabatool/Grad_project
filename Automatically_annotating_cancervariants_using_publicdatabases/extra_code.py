# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup as soup
# from urllib.request import urlopen as ureq
# import random
# import time
# import os
#
# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver_for_mac")
#
# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.default_content_setting_values.notifications": 2}
# chrome_options.add_experimental_option("prefs", prefs)
#
# # A randomizer for the delay
# seconds = 5 + (random.random() * 5)
# # create a new Chrome session
# driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.implicitly_wait(30)
# # driver.maximize_window()
#
# # navigate to the application home page
# driver.get("https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=6261085")
# time.sleep(seconds)
# time.sleep(seconds)
#
#
# # Add more to range for more phones
# # for i in range(1):
# #     element = driver.find_element_by_id("moreProduct")
# #     driver.execute_script("arguments[0].click();", element)
# #     time.sleep(seconds)
# #     time.sleep(seconds)
#
#
# html = driver.page_source
# page_soup = soup(html, "html.parser")
# print(page_soup)
# containers = page_soup.findAll("div", {"class": "column col3"})




# from urllib.request import urlopen
# sock = urlopen("")
# htmlSource = sock.read()
# sock.close()
# print (htmlSource)
#
#

# import urllib.request
#
# fp = urllib.request.urlopen("https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=6261085")
# mybytes = fp.read()
#
# mystr = mybytes.decode("utf8")
# fp.close()
#
# print(mystr)



# from bs4 import BeautifulSoup
# from urllib.request import urlopen
# import re
# import requests
# s = requests.Session()



# def fetch_page_soup(url):
#     """ Fetches page data from a URL and returns a parsed BeautifulSoup object """
#     response = None
#     try:
#        # response = urlopen(url)
#         r = s.get("https://example.net/users/101")
#         soup = BeautifulSoup(r.text)
#         #soup = BeautifulSoup(response.read(),features="html.parser")
#     finally:
#         if response:
#             response.close()

#     return soup


# def find_cosmic_cell_line(cosmic_id):
#     """ Returns a COSMIC cell line's annotation, given a COSMIC ID. """

#     url = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=6261085'
#     print(url)
#     soup = fetch_page_soup(url)
#     print(soup)

#     metadata = {}

#     #The sample metadata is stored in the "overview" tab
#     if soup.find("div", id="overview"):
#         soup = soup.find("div", id="overview").find("div", {"class":re.compile("w75")})

#         #Zip the metadata up into a dictionary
#         metadata = dict(zip([x.string for x in soup.findAll("dt")], [x.string for x in soup.findAll("dd")]))

#         #The sample name will not properly parse this way, so we have to pluck it out separately.
#         metadata["Sample name"] = soup.find(text="Sample name").findNext("dd").find("a").string

#     return metadata

# if __name__ == "__main__":

#     cosmic_id = 6261085
#     results = find_cosmic_cell_line(id)
#     print(results)
#     for k,v in results.items():
#         print ("%s\t%s"%(k,v))



# Kanza Code:

# import re
# chunks = []
# hand = open('outputSiftSymtabLAGFC_HGVSc_SOMATIC.vcf')
#
#
# for line in hand:
#     line = line.strip()
#     x = re.findall('[a-z]\s([A-Z].*)\s[a-z-].*:([a-z].+>[A-Z])', line)
#     if len(x) >0 : chunks.append(x)
#
# ID = []
# for x in chunks:
#     for a in x:
#         ID.append(a)
#
#
# URL = []
# serviceurl = 'https://clinicaltables.nlm.nih.gov/api/cosmic/v3/search?terms='
# for i in range(len(ID)):
#     a= serviceurl + ID[i][0]+'+'+ID[i][1]
#     URL.append(a)
#
# URL = [s.replace('>','%3E') for s in URL]
#
#
# from urllib.request import urlopen
# myfile =[]
# for i in range(len(URL)):
#     f = urlopen(URL[i])
#     a = f.read()
#     myfile.append(a)
#
#
# #Regex all the COSMIC IDs
# y = re.findall('COSM([0-9]{7})', str(myfile))
#
# #Retain only unique IDs
# COS_ID = list(set(y))
#
# #URL for mutation in COSMIC
# MutationURL = []
# mutationAPI = 'https://cancer.sanger.ac.uk/cosmic/mutation/overview?id='
# for i in range(len(COS_ID)):
#     a = mutationAPI + COS_ID[i]
#     MutationURL.append(a)
#
# print(MutationURL)


