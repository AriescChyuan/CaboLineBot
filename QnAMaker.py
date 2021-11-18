import requests
import json

url = "https://caboqna.azurewebsites.net/qnamaker/knowledgebases/e6f059e2-e1c1-44c8-a494-6e3a385a1979/generateAnswer"
def QnAMaker(message_text):
    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Ocp-Apim-Subscription-Key': 'dc303682-21ae-4bf1-b813-4a416a151f74'
                   }
               )

    data = response.json()

    try: 
        #我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        #這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']

        return answer
        print('answer', answer)

    except Exception:

        return "Error occurs when finding answer"