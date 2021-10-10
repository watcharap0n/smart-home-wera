from fastapi import APIRouter, Request, HTTPException, Body
from typing import Optional
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import StickerSendMessage, TextSendMessage, TextMessage, MessageEvent
import json
import os
from config.db_pymongo import MongoDB
from random import randint
from environ.heroku_environ import SECRET_LINE, ACCESS_TOKEN, set_firebase
from config.db_firebase import Config_firebase

# client = 'mongodb://127.0.0.1:27017'
config = Config_firebase(path_db=set_firebase)
fb = config.database_fb()
client = os.environ.get('MONGODB_URI')
db = MongoDB(database_name='dashboard', uri=client)
collection = 'line_bot_smart_home_kane'
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET_LINE)

router = APIRouter()


def get_profile(user_id):
    profile = line_bot_api.get_profile(user_id)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    result = {'displayName': displayName, 'userId': userId, 'img': img, 'status': status}
    return result


@router.post('/webhook')
async def webhook(
        request: Request,
        raw_json: Optional[dict] = Body(None)
):
    with open('config/line_log.json', 'w') as log_line:
        json.dump(raw_json, log_line)
    try:
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        events = raw_json['events'][0]
        _type = events['type']
        if _type == 'follow':
            userId = events['source']['userId']
            profile = get_profile(userId)
            inserted = {'displayName': profile['displayName'], 'userId': userId, 'img': profile['img'],
                        'status': profile['status']}
            db.insert_one(collection='line_follower', data=inserted)
        elif _type == 'unfollow':
            userId = events['source']['userId']
            db.delete_one('line_follower', query={'userId': userId})
        elif _type == 'postback':
            event_postback(events)
        elif _type == 'message':
            message_type = events['message']['type']
            if message_type == 'text':
                try:
                    userId = events['source']['userId']
                    message = events['message']['text']
                    profile = get_profile(userId)
                    push_message = {'user_id': userId, 'message': message, 'display_name': profile['displayName'],
                                    'img': profile['img'],
                                    'status': profile['status']}
                    db.insert_one(collection='message_user', data=push_message)
                    handler.handle(str(body, encoding='utf8'), signature)
                except InvalidSignatureError as v:
                    api_error = {'status_code': v.status_code, 'message': v.message}
                    raise HTTPException(status_code=400, detail=api_error)
            else:
                no_event = len(raw_json['events'])
                for i in range(no_event):
                    events = raw_json['events'][i]
                    event_handler(events)
    except IndexError:
        raise HTTPException(status_code=200, detail={'Index': 'null'})
    return raw_json


def event_handler(events):
    replyToken = events['replyToken']
    package_id = '446'
    stickerId = randint(1988, 2027)
    line_bot_api.reply_message(replyToken, StickerSendMessage(package_id, str(stickerId)))


def event_postback(events):
    postback = events['postback']
    replyToken = events['replyToken']
    userId = events['source']['userId']
    relay = postback['data']
    fb.child('Wera').set({'RelayBedRoom': int(relay)})
    relay = int(relay)
    package_id = '6136'
    sticker_id = randint(10551376, 10551399)
    if relay == 3 or relay == 5:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='เปิดไฟแล้วจ้า'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))
    elif relay == 4 or relay == 6:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='ปิดไฟแล้วจ้า'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))
    elif relay == 10 or relay == 8:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='เปิดแล้วจ้า'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))
    elif relay == 9 or relay == 7:
        line_bot_api.reply_message(replyToken, TextSendMessage(text='ปิดแล้วจ้า'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id=package_id, sticker_id=str(sticker_id)))


@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    text = event.message.text
    reply = event.reply_token
    print(reply)
    if text == '@ON':
        fb.child('Wera').set({'RelayBedRoom': 1})
        line_bot_api.reply_message(reply, TextSendMessage(text='เปิดไฟแล้วจ้า'))
    elif text == '@OFF':
        fb.child('Wera').set({'RelayBedRoom': 0})
        line_bot_api.reply_message(reply, TextSendMessage(text='ปิดไฟแล้วจ้า'))
