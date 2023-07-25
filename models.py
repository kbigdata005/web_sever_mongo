from pymongo import MongoClient
import datetime
# 암호화 알고리즘. 256을 제일 많이 사용한다.
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from config import MONGODB_URL

def hash_password(original_password):
    salt = 'eungok'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password

def check_password(input_password, hashed_password):
    salt = 'eungok'
    password = input_password + salt
    result = pbkdf2_sha256.verify(password , hashed_password)
    return result

class MyMongo:

    def __init__(self , db_url , database):
        self.database = database
        self.client = MongoClient(db_url)

    def user_insert(self , username, email, phone, password):
        db = self.client.os
        users = db.users
        pw = hash_password(password)
        user = {
            "username":username,
            "email":email,
            "phone":phone,
            "password":pw,
            "create_at":datetime.datetime.utcnow()
        }
        result = users.insert_one(user)
        print(result)
        return 1
    
    def verify_password(self,input_password,  email):
        db = self.client.os
        users = db.users
        user = users.find_one({'email':email})
        # print(user)
        if user:
            result = check_password(input_password , user['password'])
            if result:
                print("Verify Success")
                return "1"
            else:
                print("Verify Fail")
                return "2"
        else:
            print("id isnot Founded")
            return "3"
    
    def find_user(self, email):
        db = self.client.os
        users = db.users
        user = users.find_one({'email':email})
        print(type(user))
        return user
    
    def find_data(self):
        db = self.client.os
        lists = db.lists
        list = lists.find()
        # for i in list:
        #     print(i)
        return list
    
    def find_one_data(self , ids):
        db =self.client.os
        list = db.lists
        data = list.find_one({'_id':ObjectId(ids)})
        return data

    def insert_data(self, title, desc, author):
        db = self.client.os
        list = db.lists
        data = {
            'title':title,
            'desc':desc,
            'author':author,
            'create_at':datetime.datetime.utcnow()
        }      
        list = list.insert_one(data)
        # for i in list:
        #     print(i)
        return list
    def delete_data(self, id):
        db = self.client.os
        list = db.lists
        list.delete_one({'_id': ObjectId(id)})
        return "1"
    
    # [컬렉션 객체].update_one( { [조건값] }, {"$set":{수정값}} )
    # knowledge_it.update_one({"author":"Dave"}, {"$set":{"text":"Hi Dave"}})
    def update_data(self,id ,title, desc ):
        db = self.client.os
        list = db.lists
        list.update_one({'_id': ObjectId(id)}, {"$set":{"title":title ,"desc": desc}})
        return "1"
# mymongo = MyMongo(MONGODB_URL , 'os')
# # mymongo.user_insert("KIM", "2@naver.com", "010-1111-1111", "1234")
# mymongo.verify_password("12343232",ObjectId('64ba2af7b26ddf90ce9642ac'))
# mymongo.find_user("1@naver.com")
# mymongo.find_data()
# mymongo.update_data("64bf3369c3a372b1fb3a29e3" , "김태경", "광산 김씨가 김해 김씨보다 쌍놈이다")

# 원문 비밀번호를, 암호화 하는 함수


# def verify_password(self, password, hashed_password):        
#         result = check_password(password, hashed_password)
#         return result
# # 방법1 - URI
# mongodb_URI = MONGODB_URL
# client = MongoClient(mongodb_URI)

# # print(client.list_database_names())

# db = client.os
# users = db.users
# result = hash_password('1234')
# user = {
#     "username":"김태경",
#     "email":"1@naver.com",
#     "phone":"010-0000-0000",
#     "password":result,
#     "create_at":datetime.datetime.utcnow()
# }


# # result = users.insert_one(user)

# # print(result)

# # user = users.find()
# # continents = [continent for continent in user]
# # print(continents[0]['_id'])

# user = users.find_one({'_id':ObjectId('64ba22e3b07d1e5e567fae07')})
# print(user)

