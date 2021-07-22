import requests
from selenium import webdriver
import re

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(options=option)

links = []
url_text_file = open("url_text_file.txt",'w')
email_text_file = open("email_text_file.txt",'w')

email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

email_list = []

domain_source = input("Enter a domain to perform passive recon on : ")

driver.get(domain_source)
elems = driver.find_elements_by_xpath("//a[@href]") #Gives a list of all links
for elem in elems:
    temp_link = elem.get_attribute("href")
    links.append(temp_link)
    print(temp_link)
    url_text_file.write(temp_link)
    url_text_file.write("\n")
    
    #Scrap for emails in the page
    for re_match in re.finditer(email_regex,driver.page_source):
        if re_match.group() not in email_list:
            email_list.append(re_match.group())
            email_text_file.write(re_match.group())
            email_text_file.write("\n")

for i in links:
    driver.get(i)
    sublink_list = driver.find_elements_by_xpath("//a[@href]") #Gives a list of all sublinks
    
    for temp_sublink in sublink_list:
        sublink = temp_sublink.get_attribute("href")
        if sublink not in links and domain_source in sublink:
            links.append(sublink)
            print(sublink)
            url_text_file.write(sublink)
            url_text_file.write("\n")
            
            #Scrap for emails in the page
            for re_match in re.finditer(email_regex,driver.page_source):
                if re_match.group() not in email_list:
                    email_list.append(re_match.group())
                    email_text_file.write(re_match.group())
                    email_text_file.write("\n")

url_text_file.close()
driver.close()