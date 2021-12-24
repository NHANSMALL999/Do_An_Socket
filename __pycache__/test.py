e ="""
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
#for row in cursor.execute("select MaNT, MuaTienMat, MuaChuyenKhoan, Ban from EXCHANGE_RATE_DATA where ThoiGian = ? AND TenNgoaiTe = ?",time, TenNgoaiTe):
#for row in cursor.execute("select * from ? where ID = ?", tablename, TenNgoaiTe)  :
#for row in cursor.execute("select MaNT, MuaTienMat, MuaChuyenKhoan, Ban from , table, "where TenNgoaiTe = ?",TenNgoaiTe):
list = []
for row in cursor.execute("select * from EXCHANGE_RATE_DATA where ThoiGian = ?",time):
#for row in cursor.execute("select TenNgoaiTe, MaNT, MuaTienMat, MuaChuyenKhoan, Ban from EXCHANGE_RATE_DATA where ThoiGian = ?",time):        
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
print(list[10])
"""



from bs4 import BeautifulSoup
#import urllib.request
import requests
import pyodbc
#try:
#    import xml.etree.cElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET


#key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDEyMjUzMjIsImlhdCI6MTYzOTkyOTMyMiwic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.GCuaOuLwvMWisYtqiVFu56Oo_xl_Y6bV-jPfiv_wRgE"
#url= "https://portal.vietcombank.com.vn/en-Us/Corporate/TG/Pages/exchange-rate.aspx?devicechannel=default"
#url = 'https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx'
#url = "https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate"
#response.status_code
#tree = xml.etree.ElementTree.fromstring(string_xml)
#xml.etree.ElementTree.dump(tree)
#req = urllib.request.urlopen(url)
#xml = BeautifulSoup(req, 'xml')
#print(xml)
#list = []
#for item in xml.find_all('Exrate'):
#    list.append(item)
#    print(item)

#print(list)





#Hàm gửi ngày tháng cho client
l = """
conx = pyodbc.connect(
"Driver={ODBC Driver 17 for SQL Server};"
"Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
"Database=EXCHANGE_RATE;"
"Trusted_Connection=yes;")
cursor = conx.cursor()
list = []
for row in cursor.execute("select ThoiGian from EXCHANGE_RATE_DATA where MaNT = ?","AUD"):
    list.append(row[0])
print(list)
conx.close()
"""

def InsertCurrencyToSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan):
    i = 0
    for data in list_TenNT:
        cursor.execute("insert EXCHANGE_RATE_DATA values (?,?,?,?,?,?)", list_ThoiGian[0], list_TenNT[i], list_MaNT[i], list_MuaTienMat[i], list_MuaChuyenKhoan[i], list_Ban[i])
        i = i+1
        conx.commit() 

def UpDateCurrencyInSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan):
    i = 0
    for data in list_MaNT:
        cursor.execute("UPDATE EXCHANGE_RATE_DATA SET TenNgoaiTe=?,MaNT=?,MuaTienMat=?,MuaChuyenKhoan=?,Ban=? where ThoiGian=? AND MaNT = ?",
        list_TenNT[i], 
        list_MaNT[i], 
        list_MuaTienMat[i], 
        list_MuaChuyenKhoan[i], 
        list_Ban[i],
        list_ThoiGian[0],
        list_MaNT[i])
        i = i + 1
        conx.commit()

def CrawlDataFromWeb():
    url = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
    try:
        response = requests.get(url)
    #Không thể gửi request tới trang web
    except:
        print("CAN NOT CONNECT TO WEBSITE!!!")
    
    #Hiển thị dưới dạng xml
    soup = BeautifulSoup(response.text, features="lxml")


    list_ThoiGian = []
    list_TenNT = []
    list_MaNT = []
    list_MuaTienMat = []
    list_MuaChuyenKhoan = []
    list_Ban = []

    ### Crawl thời gian ###
    
    tag = soup.find("datetime")
    list_ThoiGian.append(tag.next)
    list_ThoiGian = [w[:10] for w in list_ThoiGian] #Tách string trong list từ ['12/23/2021 1:21:55 PM'] thành ['12/23/2021']

    ### Crawl tỷ giá tiền tệ ###
    for tag in soup.find_all("exrate"):
        list_TenNT.append(tag.get("currencyname"))
        list_MaNT.append(tag.get("currencycode"))
        list_MuaTienMat.append(tag.get("buy"))
        list_MuaChuyenKhoan.append(tag.get("transfer"))
        list_Ban.append(tag.get("sell"))
        
    ### Tạo kết nối ###
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
    cursor = conx.cursor()

    check = ""
    MaNT = "USD"

    #Kiểm tra nếu data của ngày đó đã có trong csdl thì check = "exist"
    for row in cursor.execute("select * from EXCHANGE_RATE_DATA where ThoiGian = ? AND MaNT = ?", list_ThoiGian[0], MaNT):
        check = "exist"
    
    #Chưa có dữ liệu của ngày ... thì insert
    if(check != "exist"):
        InsertCurrencyToSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan)
   
    #Nếu ngày ... đã có dữ liệu rồi thì update
    else:
        UpDateCurrencyInSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan)    
    
    conx.close()        

   
        
        
#print(list_ThoiGian)    
#print(list_TenNT)   
#print(list_MaNT)
#print(list_MuaTienMat)
#print(list_MuaChuyenKhoan)
#print(list_Ban)
        
        
        
        
        
        
        
        
    #list.append(tag)
    #print(list)    
    #print(tag.get("currencycode"))
    #print(tag.get("currencyname"))
    #print(tag.get("buy"))
    #print(tag.get("transfer"))
    #print(tag.get("sell"))
#print(response.content)     
#content = []
#result = bs_content.find("AUSTRALIAN DOLLAR")
##print(bs_content)
#print(result)
##soup = BeautifulSoup(response.content,"html.parser")
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