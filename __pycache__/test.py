c="""
import socket
import threading
mport pyodbc #thêm thư viện để kết nối với sql
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
"""






from bs4 import BeautifulSoup
import requests


#try:
#    import xml.etree.cElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET


#key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDEyMjUzMjIsImlhdCI6MTYzOTkyOTMyMiwic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.GCuaOuLwvMWisYtqiVFu56Oo_xl_Y6bV-jPfiv_wRgE"

#url= "https://portal.vietcombank.com.vn/en-Us/Corporate/TG/Pages/exchange-rate.aspx?devicechannel=default"
#url = 'https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx'
#url = "https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate"
url = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
response = requests.get(url)
response.status_code
#soup = BeautifulSoup(response.text, features="lxml")
##soup.title.string
#for tag in soup.find_all('a'):
#    print(tag.get("href"))
#print(response.content)     

#content = []

#result = bs_content.find("AUSTRALIAN DOLLAR")
#print(bs_content)
#print(result)
#soup = BeautifulSoup(response.content,"html.parser")

#for child_of_root in root:
#    print(root.attrib)
#    print(root.tag)
#print(soup)
#print(response.content)



s = """
#Hàm nhận danh sách
def RecieveList(client, list):
    list = []
    data = None
    data= client.recv(1024).decode(FORMAT)
    while(data!="end"):
        list.append(data)
        conn.send(data.encode(FORMAT))
        data= conn.recv(1024).decode(FORMAT)
    return list
#Hàm nhận toàn bộ bảng data từ server
def GetAllDataFromServer(client,list):
    RecieveList(client, list)

#Hàm nhận data theo tên từ server
def GetSpeDataFromServer(client, list):
    RecieveList(client, list)
    def click_X(self,client):
        if messagebox.askyesno("Exit", "Do you want to quit the app?"):
            # Them cac chuc nang khac trong nay
            client.send("0".encode(FORMAT))
            client.recv(1024)
            client.close
            ###################################
            self.destroy()
"""