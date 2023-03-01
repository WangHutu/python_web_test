import db


def getList():
    list = db.getDbData('web_system_db', 'board_list')
    print(list, 'board_list')