import pandas as pd
from typing import List
from fastapi import Depends, FastAPI, HTTPException
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



data = pd.read_excel (r'C:\Users\Nagababu\Documents\Urls.xls') 
pds = pd.DataFrame(data)
productsdata = pd.read_excel (r'C:\Users\Nagababu\Documents\products.xls') 
product = pd.DataFrame(productsdata)
# , columns= ['urls']
searchProducts = product['products'].tolist()
urlsList = pds['urls'].tolist()




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



@app.get('/scrapper')
def get_scrapper_data():
    # productDetails = db.query(models.Movie).filter(models.Movie.title.contains(search)).all()
    return searchProducts
