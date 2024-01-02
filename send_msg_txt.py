import datetime
import requests, json
import base64
import hashlib
import schedule
import time
import random
import os

meituan_date = 18

def wx_image():
    wx_dir = './images/week_record/'
    images_array = os.listdir(wx_dir)
    image = wx_dir + random.choice(images_array)
    return sendMsg(image)


def meituan_image():
    ts = datetime.date.today()
    if ts.day != meituan_date:
        return

    meituan_dir = './images/18th/'
    images_array = os.listdir(meituan_dir)
    image = meituan_dir + random.choice(images_array)
    return sendMsg(image)


def meituan_13_image():
    wx_dir = './images/13yuan/'
    images_array = os.listdir(wx_dir)
    image = wx_dir + random.choice(images_array)
    return sendMsg(image)

def sendMsg(image):
    with open(image, 'rb') as file:
        data = file.read()
        encodestr = base64.b64encode(data)
        image_data = str(encodestr, 'utf-8')

    with open(image, 'rb') as file:  # gif=-md5
        md = hashlib.md5()
        md.update(file.read())
        image_md5 = md.hexdigest()

    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=53f6f927-8c49-48e0-8957-97b344b1db8d"
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "image",
        "image": {
            "base64": image_data,
            "md5": image_md5
        }
    }

    result = requests.post(url, headers=headers, json=data)
    return result


# wx_image()
# 周报提醒
schedule.every().friday.at("17:00").do(wx_image)
# 美团18号18元大额劵提醒
schedule.every().day.at("10:55").do(meituan_image)
# 美团星期一二 13元大额劵提醒
schedule.every().monday.at("10:58").do(meituan_13_image)
schedule.every().tuesday.at("10:58").do(meituan_13_image)

while True:
    schedule.run_pending()
    time.sleep(60)