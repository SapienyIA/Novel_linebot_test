from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import json
import syosetu_crawler as sc



app = Flask(__name__)
ac = {}
with open("./account", 'r') as file:
     for line in file.readlines():
         line = line.strip()
         ac[line.split('=')[0]]=line.split('=')[1]
line_bot_api = LineBotApi(ac['token'])
handler = WebhookHandler(ac['secret'])
cmd =  ['@即時查詢','@列出清單','@新增小說','@刪除小說','tmp']


@app.route("/")
def home():
  try:
    msg = request.args.get('msg')
    if msg != None:
      line_bot_api.push_message(ac['uid'], TextSendMessage(text=msg))
      return msg
    else:
      return 'OK'
  except:
    print('route error')



@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text']
        if msg == cmd[0]:
            msg2 = sc.check_update()
        elif msg == cmd[1]:
            msg2 = sc.list_query()
        elif msg == cmd[2]:
            msg2 = "請輸入要新增的網址"
        elif msg == cmd[3]:
            msg2 = "請輸入要刪除的小說名稱"
        else:
            if cmd[4] == cmd[2]:
                try:
                    msg2 = sc.book_add(msg)
                except:
                    msg2 = "輸入網址有誤"
            elif cmd[4] == cmd[3]:
                try:
                    msg2 = sc.book_remove(msg)
                except:
                    msg2 = "輸入書本有誤"
            else:
                msg2 = "指令錯誤"
        cmd[4] = msg
        line_bot_api.reply_message(tk,TextSendMessage(text=msg2))
    except:
        print('linebot error')
    return 'OK'

def run_server():
    app.run()
