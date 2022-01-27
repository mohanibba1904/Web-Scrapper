import pandas as pd
from typing import List
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.sql.expression import and_, null
from sqlalchemy.sql.functions import user
from sharedlibrary import crud,models, schemas
from datetime import datetime, timedelta 
from sharedlibrary.database import SessionLocal, engine
from typing import Optional
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from xlwt import *
import os
# import xlrd
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)
# wb = xlrd.open_workbook('C:/Users/Nagababu/Documents/products.xls')
app = FastAPI()
origins = [
    "http://127.0.0.1:8000/login",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=1500)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    

pwd_context= CryptContext(schemes=["bcrypt"],deprecated='auto')



# workbook = Workbook(encoding = 'utf-8')
# table = workbook.add_sheet('data')
# table.write(0, 0, 'S.no')
# table.write(0, 1, 'Names')
# table.write(0, 2, 'Investing')
# table.write(0, 3, 'Mcx')
# table.write(0, 4, 'economictimes')
# table.write(0, 5, 'markets-businessinside')
# table.write(0, 6, 'tradingeconomics')

# data = pd.read_excel (r'C:\Users\Nagababu\Documents\Urls.xls') 
# pds = pd.DataFrame(data)
# productsdata = pd.read_excel (r'C:\Users\Nagababu\Documents\products.xls') 
# product = pd.DataFrame(productsdata)
# # , columns= ['urls']
# searchProducts = product['products'].tolist()
# urlsList = pds['urls'].tolist()




# @app.get("/users_details/")
# def read_users(db: Session = Depends(get_db)):
#     usersDetails = db.query(models.User).all()
#     return usersDetails


# @app.get("/users_details/{user_id}")
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id==user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user



# # @app.get("/login")
# # def read_item(user_name:str, password:str,db: Session = Depends(get_db)):
# #     users = crud.get_users(db)
# #     us = ''
# #     ps= ''
# #     for i in users:
# #         if(i.user_name == user_name):
# #             us = i.user_name
# #             ps = i.password
# #     if user_name == us:
# #         if str(ps) == password:
# #             payload_data = {"user_name": user_name}
# #             encoded_jwt = jwt.encode(payload=payload_data, key="secreat")
# #             s['auth'].append(encoded_jwt)
# #             return("login success", encoded_jwt)
# #         else:
# #             return("username and password not matched")

# #     else:
# #         return("login error")

# @app.post('/signup')
# def create_user(request:schemas.User,db: Session = Depends(get_db)):
#     hashedPassword=pwd_context.hash(request.password)
#     new_user=models.User(user_name=request.user_name, email=request.email,password=hashedPassword)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.post('/login')
# def login(request:schemas.Data,db:Session= Depends(get_db)):
#     current_user=db.query(models.User).filter(models.User.user_name == request.user_name).first()
#     # user_id=db.query(models.User.id).filter(models.User.user_name == request.user_name).first()
#     hashedPassword = current_user.password
#     is_valid=pwd_context.verify(request.password, hashedPassword)
#     if is_valid:
#         access_token = create_access_token(data={"sub": current_user.user_name,"user_id": current_user.id})
#         return{"access_token":access_token, "token_type":"bearer"}
#     return "user not found"





# @app.get('/movies')
# def get_movie(search: Optional[str] ,db: Session = Depends(get_db) ):
#     productDetails = db.query(models.Movie).filter(models.Movie.title.contains(search)).all()
#     return productDetails



# @app.get("/movies/movieid/{movie_id}")
# def get_movie_id(movie_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(models.Movieid).filter(models.Movieid.id== movie_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user    
# # class Test():
# #     user: str

# # @app.post("/test")
# # def test(user:Test):
#     # return user

# @app.get("/favourite")
# def join(token: jwt = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     user_id: str = payload.get("user_id")
#     db_user = db.query(models.Favoritemovies.movie_id).filter(models.Favoritemovies.user_id== user_id).all()
#     lists = []
#     if db_user is not null:
#         for i in db_user:
#             my = db.query(models.Movie).filter(models.Movie.id== i.movie_id).first()
#             lists.append(my)
#         return lists

#     else:
#         return lists
#     # if user_id in db_user:
#     #     for i in db_user:
#     #         if()
#     #     my = db_user.filter(movie_id)
#     #     mv = db.query(models.Movie).filter(models.Movie.movie_id).all()
#     #     return mv
#     # # db_user = db.query(models.User).filter(models.User.id==1).first()
#     # # join =  [db.query(models.User(id=1)), db.query(models.Movie(id=1))]
#     # # value = crud.like_a_join(movie_id= movie_id,user_id= user_id,db=db)
#     # else:
    
    




# @app.post("/CreateFavourite/{movie_id}")
# def create(movie_id: int,db:Session=Depends(get_db),token: jwt = Depends(oauth2_scheme)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     user_id: int = payload.get("user_id")
#     add_fav= models.Favoritemovies(user_id=user_id,movie_id=movie_id)
#     db.add(add_fav)
#     db.commit()
#     db.refresh(add_fav)
#     return add_fav


# # @app.post("/CreateFavourite")
# # def create(request:schemas.Favouritedata,db:Session=Depends(get_db)):
# #     add_fav= models.Favoritemovies(user_id=request.user_id,movie_id=request.movie_id)
# #     db.add(add_fav)
# #     db.commit()
# #     db.refresh(add_fav)
# #     return add_fav






# @app.delete('/favouritedelete/{movie_id}')
# def del_fav(movie_id: int,token: jwt = Depends(oauth2_scheme),db:Session=Depends(get_db)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     user_id: str = payload.get("user_id")
#     db.query(models.Favoritemovies).filter(and_(models.Favoritemovies.user_id == user_id, models.Favoritemovies.movie_id == movie_id)).delete(synchronize_session=False)
#     db.commit()
#     return 'done'  

workbook = Workbook(encoding = 'utf-8')
table = workbook.add_sheet('data')
table.write(0, 0, 'S.no')
table.write(0, 1, 'Names')
table.write(0, 2, 'Investing')
table.write(0, 3, 'Mcx')
table.write(0, 4, 'economictimes')
table.write(0, 5, 'markets-businessinside')
table.write(0, 6, 'tradingeconomics')

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
        


def specificUrl(index,searchProducts,urlsList):
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


path = 'C:/Users/Nagababu/Documents/GitHub/Web-Scrapper'
def craweler(searchProducts):
    
    data = pd.read_excel (r'C:\Users\Nagababu\Documents\Urls.xls') 
    pds = pd.DataFrame(data)
    # productsdata = pd.read_excel (r'C:\Users\Nagababu\Documents\products.xls') 
    # product = pd.DataFrame(productsdata)
    # , columns= ['urls']
    # searchProducts = product['products'].tolist()
    urlsList = pds['urls'].tolist()




    # searchProducts =  ['silver mini','gold', 'platinum','nickel',  'silver micro', 'nickel mini', 'aluminium', 'lead',  'copper mini']
    row = 1
    finalresult = []
    for i in range(len(urlsList)):
        finalresult.append(specificUrl(i,searchProducts,urlsList))
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
    workbook.save('MultipleUrlsScrapying.xls')  
    file_path = os.path.join(path, 'api/MultipleUrlsScrapying.xls')
    return FileResponse(file_path, filename='scraping.xls')




@app.post('/scrapper')
async def get_scrapper_data(file: UploadFile = File(...)):
    # productDetails = db.query(models.Movie).filter(models.Movie.title.contains(search)).all()

    data = pd.read_excel(file.file.read())
    product = pd.DataFrame(data)
    # , columns= ['urls']
    searchProducts = product['products'].tolist()
    result = craweler(searchProducts)
    return result
