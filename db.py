import pymongo
myclient = pymongo.MongoClient('mongodb://localhost:27017')

def verify_db(db, collection):
    list = myclient.list_database_names()
    if list:
        if  db in list:
            return True
        else:
            newdb = myclient[db]
            collection = newdb[collection]
    else:
        newdb = myclient[db]
        collection = newdb[collection]

# print(myclient.list_database_names())

# 插入数据
def insertDbData(db, collection, data):
    verify_db(db, collection)
    if collection == 'users':
        user = getDbData(db, collection, {"user" : data.get('user')})
        print(user)
        if not user:
            myclient[db][collection].insert_one(data)
            return True
        else:
            return False
    
# 查询数据
def getDbData(db, collection, data):
    return myclient[db][collection].find_one(data)
