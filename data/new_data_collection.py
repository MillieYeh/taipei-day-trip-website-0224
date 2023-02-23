import json
import mysql.connector
from encodings import utf_8

def db_connection():
    mydb = None
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        database = "travel",
        password = "cycycy1018==",
        charset = "utf8"
        )
    except mysql.connector.Error as e:
        print(e)
    return mydb

mydb = db_connection()
mycursor = mydb.cursor()

def stringToList(string):
    listRes = list(string.split(" "))
    return listRes

data = open('taipei-attractions.json', 'r', encoding='utf-8').read()
obj = json.loads(data)
information = obj["result"]["results"]

for i in information:
    data_1 = []
    id = i["_id"]
    name = i["name"]
    category = i["category"]
    description = i["description"]
    address = i["address"].replace(' ', '')
    transport = i["transport"]
    mrt = i["mrt"]
    lat = i["lat"]
    lng = i["lng"]
    
    imgs = i["file"].split('http')
    pic_list=[]
    for j in imgs:
        my_suffixes = ("JPG", "PNG", "jpg", "png")
        if j.endswith(my_suffixes) != True  or  j == '' :
            continue
        pic='http'+ j
        pic_list.append(pic)
    pic_list = str(pic_list)
    
    # 會產生很多多於符號
    # image.pop(0)
    # output = []
    # for j in image:
    #     total = 'https' + j
    #     last = j.split('.')[-1].lower()
    #     if last == 'jpg' or last == 'JPG' or last == 'png' or last == 'PNG':
    #         https = "https"
    #         output.append("https" + j)
    #         image_list = output
    #         images_json = json.dumps(image_list)
            
    sql = """
        INSERT INTO attractions (id, name, category, description, address, transport, mrt, lat, lng, imgs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (id, name, category, description, address, transport, mrt, lat, lng, pic_list, )
    mycursor.execute(sql, val)        
    mydb.commit()
mydb.close()