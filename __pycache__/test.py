import requests
#Import module này để phân tích tệp xml
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
#lấy dữ liệu từ web
#{"results":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDA5MTA5MzEsImlhdCI6MTYzOTYxNDkzMSwic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.tRBpbaJ_y9Stl_SGXjxt15PhqVH5LNTRMl4veqWC0qU"}

response = requests.get("https://portal.vietcombank.com.vn/Personal/TG/Pages/ty-gia.aspx?devicechannel=default")
#response = requests.get("https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx")
soup = BeautifulSoup(response.content, "html.parser")

tree = ET.ElementTree(soup)
print(tree)
root = tree.getroot()
#print(root)
for child_of_root in root:
    print(child_of_root.tag)
#print(tree)
#root = tree.getroot()
#for child_of_root in root:
#    print(child_of_root.tag)
#make it more beautifull

#Lấy dữ liệu mình cần
#print("##############################################################################################################")
#data = soup.find_all('h3', class_='title-news')
#print(data)