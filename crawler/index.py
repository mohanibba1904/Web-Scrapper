
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from xlwt import *
import pandas as pd


data = pd.read_excel (r'C:\Users\Nagababu\Documents\Urls.xls') 
pds = pd.DataFrame(data)
productsdata = pd.read_excel (r'C:\Users\Nagababu\Documents\products.xls') 
product = pd.DataFrame(productsdata)
# , columns= ['urls']
searchProducts = product['products'].tolist()
urlsList = pds['urls'].tolist()


workbook = Workbook(encoding = 'utf-8')
table = workbook.add_sheet('data')
table.write(0, 0, 'S.no')
table.write(0, 1, 'Names')
table.write(0, 2, 'Investing')
table.write(0, 3, 'Mcx')
table.write(0, 4, 'economictimes')
table.write(0, 5, 'markets-businessinside')
table.write(0, 6, 'tradingeconomics')

# searchProducts =  ['silver mini','gold', 'platinum','nickel',  'silver micro', 'nickel mini', 'aluminium', 'lead',  'copper mini']

def urlFunction(url,index):
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36'
        }
    strval = ''
    if(index==0):      
        status = requests.get(url,headers=headers,allow_redirects=False)
        strval = str(status)
    elif(index==1):
        status = requests.get(url) 
        strval = str(status) 
    elif(index==2):
        status = requests.get(url) 
        strval = str(status)
    elif(index==3):
        status = requests.get(url) 
        strval = str(status) 
    elif(index==4):
        status = requests.get(url) 
        strval = str(status)              
    print(status)
    if('<Response [200]>'==strval):
        # C:\Users\Nagababu\Downloads\chromedriver_win32\chromedriver.exe'
        driver = webdriver.Chrome(r'C:\chromedriver.exe')
        driver.get(url) 
        # this is just to ensure that the page is loaded
        
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        driver.close()
        if(index==0):
            all_divs = soup.find('div',{
                    'class': ['last u-up' ,'last u-down']
                }).find('bdo')               
            v = all_divs.text
            print(v)
            return v
        elif(index==1):
            all_divs = soup.find('td',{
                    'class': "commonopen"
                })
            return  all_divs.text
        elif(index==2):
            
            all_divs = soup.find('section',{
                'id': 'pageContent'
            }).find('span',{
                'class':"commodityPrice"
            })
            val = all_divs.text 
            print(val) 
            return val

        elif(index==3):
            all_divs = soup.find('span',{
                'class':"price-section__current-value"
            })
            val = all_divs.text 
            print(val) 
            return val 
        elif(index==4):
            all_divs = soup.find('span',{
                'class':"closeLabel"
            })
            val = ''
            if(all_divs==None):
                val = None
            else:
                val = all_divs.text    
            return val        
    else:
        
        return None
        


def specificUrl(index):
    if(index==0):
        investingPrice = []
        for ym in searchProducts:
            Urls = urlsList[index] + ym.replace(' ','-')
            fun = urlFunction(Urls,index)
            if(fun==None):
                investingPrice.append('Not Found')
            else:
                investingPrice.append(fun)    
        return investingPrice

    elif(index==1):       
        priceslist = []
        for ym in searchProducts:
            Urls = urlsList[index] + ym.replace(' ','-')
            fun = urlFunction(Urls,index)
            if(fun==None):
                priceslist.append('Not Found')
            else:
                priceslist.append(fun.strip())    
        return priceslist

    elif(index==2):        
        priceslist = []
        for ym in searchProducts:
            val = ym.upper()
            Urls = urlsList[index] + val.replace(' ','') + '.cms'
            print(Urls)
            fun = urlFunction(Urls,index)
            if(fun==None):
                priceslist.append('Not Found')
            else:
                priceslist.append(fun.strip())   
        return priceslist

    elif(index==3):        
        priceslist = []
        for ym in searchProducts:
            Urls = urlsList[index] + ym.replace(' ','-') + '-price'
            print(Urls)
            fun = urlFunction(Urls,index)
            if(fun==None):
                priceslist.append('Not Found')
            else:
                priceslist.append(fun.strip())    
        return priceslist

    elif(index==4):        
        priceslist = []
        for ym in searchProducts:
            Urls = urlsList[index] + ym.replace(' ','-')
            print(Urls)
            fun = urlFunction(Urls,index)
            if(fun==None):
                priceslist.append('Not Found')
            else:
                priceslist.append(fun.strip())    
        return priceslist    

row = 1
finalresult = []
for i in range(len(urlsList)):
    finalresult.append(specificUrl(i))
for my in range(len(searchProducts)):
        name = searchProducts[my]
        v1 = finalresult[0][my]
        v2 = finalresult[1][my]
        v3 = finalresult[2][my]
        v4 = finalresult[3][my]
        v5 = finalresult[4][my]
        table.write(row, 0, row)
        table.write(row, 1, name) 
        table.write(row, 2, v1) 
        table.write(row, 3, v2)  
        table.write(row, 4, v3) 
        table.write(row, 5, v4)  
        table.write(row, 6, v5)  
 
        row+=1 
workbook.save('MulipleUrlsScrapying.xls')  
