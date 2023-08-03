from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    UserSource
)
import os
import requests
import re
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if text == 'profile':
            if isinstance(event.source, UserSource):
                profile = line_bot_api.get_profile(user_id=event.source.user_id)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            TextMessage(text='Display name: ' + profile.display_name),
                            TextMessage(text='Status message: ' + str(profile.status_message))
                        ]
                    )
                )
        elif text == '正妹' or text.lower() =='beauty' or text == '抽' or text == "美女" or text == "振銓前女友":

            response = requests.get('https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&forumdisplay=&page=1')
            soup = BeautifulSoup(response.text, 'html.parser')
            # max_page = soup.find_all('label')[0].find('span').string.split(' ')[2]
            max_page = int(soup.find_all(title=re.compile('共\s\d+\s頁'))[0].string.split(' ')[2])
            random_page = random.randint(1, int(max_page)-2)

            # url = f"https://www.jkforum.net/forum-736-{random_page}.html"
            url = f"https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&forumdisplay=&page={random_page}"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            images = soup.find_all("img", src=re.compile("https://www.my"))[:-3]
            images_len = len(images)
            image_url = soup.find_all("img", src=re.compile("https://www.my"))[:-3][random.randint(0, images_len-1)].get("src")

            # line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
            ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=image_url, preview_image_url=image_url)
                    ]
                )
            

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)