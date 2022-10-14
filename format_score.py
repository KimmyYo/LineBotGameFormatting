
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, 
    FollowEvent,
    TextMessage, 
    TextSendMessage, 
    TemplateSendMessage, 
    ButtonsTemplate, 
    MessageTemplateAction, 
    PostbackEvent,
    PostbackTemplateAction)
import json
from datetime import datetime

ALLOWED_HOSTS = [
    'e436-140-117-191-193.jp.ngrok.io'
]

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_BOT_AUTH_TOKEN)
handler = WebhookHandler(LINE_BOT_SECRET)


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

full_format_msg = []

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    full_format_msg.append(user_text)
    if user_text == "哈囉美女":
        user_id = event.source.user_id
        line_bot_api.push_message(user_id, TextSendMessage(text="請依序輸入：場次、隊名、分數。輸入結束後打上「美女謝謝」"))
        full_format_msg.clear()
    
    if user_text == "美女謝謝":

        num_of_game = full_format_msg[0]
        team_win = full_format_msg[1]
        team_lost = full_format_msg[2]
        first_round = full_format_msg[3]
        second_round = full_format_msg[4]
        third_round = full_format_msg[5]
        today = datetime.now().strftime("%m/%d")
        if third_round == "美女謝謝":
            game_result = f"場次{num_of_game}，{today}，{team_win}vs{team_lost}，{first_round}，{second_round}，{team_win}勝"
        else:
            game_result = f"場次{num_of_game}，{today}，{team_win}vs{team_lost}，{first_round}，{second_round}，{third_round}，{team_win}勝"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=game_result))
        full_format_msg.clear()
        





# @app.route('/')
# def index():
#     return 'Hello World'

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


