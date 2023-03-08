import pymongo
myclient = pymongo.MongoClient('mongodb://localhost:27017')

def verify_db(db, collection):
    list = myclient.list_database_names()
    if not list or db not in list:
        newdb = myclient[db]
        collection = newdb[collection]
        

# 插入数据
def insertDbData(db, collection, data):
    verify_db(db, collection)
    if collection == 'users':
        user = getDbData(db, collection, {"user" : data.get('user')})
        if not user:
            myclient[db][collection].insert_one(data)
            return True
        else:
            return False
    
# 查询数据
def getDbData(db, collection, data):
    print(data, 'ddddaaaattttaaaaa')
    if (data):
        print('数据库查出的数据', myclient[db].get_collection(collection).find(data))
        return myclient[db].get_collection(collection).find(data)
    else:
        print('数据库查出的数据', myclient[db][collection].find())
        return myclient[db][collection].find()
