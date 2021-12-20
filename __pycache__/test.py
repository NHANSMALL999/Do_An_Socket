import socket
import threading
import pyodbc #thêm thư viện để kết nối với sql
PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

LOGIN="logIn"
SIGNUP="signUp"
table = "EXCHANGE_RATE_9_12_21"   

conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
cursor = conx.cursor()
TenNgoaiTe = "SAUDI RIAL"

prefix = "dbo"
tablename = "EXCHANE_RATE_9_12_21"
time = "09/12/2021"
for row in cursor.execute("select MaNT, MuaTienMat, MuaChuyenKhoan, Ban from EXCHANGE_RATE_DATA where ThoiGian = ? AND TenNgoaiTe = ?",time, TenNgoaiTe):
#for row in cursor.execute("select * from ? where ID = ?", tablename, TenNgoaiTe)  :
#for row in cursor.execute("select MaNT, MuaTienMat, MuaChuyenKhoan, Ban from , table, "where TenNgoaiTe = ?",TenNgoaiTe):
        #print(row)
        list = []
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        print(list)




t="""
from bs4 import BeautifulSoup
import requests
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDEyMjUzMjIsImlhdCI6MTYzOTkyOTMyMiwic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.GCuaOuLwvMWisYtqiVFu56Oo_xl_Y6bV-jPfiv_wRgE"

#url= "https://portal.vietcombank.com.vn/en-Us/Corporate/TG/Pages/exchange-rate.aspx?devicechannel=default"
#url = 'https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx'
#url = "https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate"
#url = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
response = requests.get(url)
#soup = BeautifulSoup(response.content,"html.parser")

#for child_of_root in root:
#    print(root.attrib)
#    print(root.tag)
#print(soup)
print(response.content)
"""
