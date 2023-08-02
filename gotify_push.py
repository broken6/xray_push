from flask import Flask, request
import datetime
import logging
import requests

app = Flask(__name__)

def push_gotify(content):
    # 替换为你的 Gotify API 地址和 API Token
    gotify_url = "http://101.42.9.79:666/message?token=AGWr1c47e8n2jYX"

    data = {
        "message": content,
    }

    try:
        response = requests.post(gotify_url, json=data)
        response.raise_for_status()
        print("Gotify notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Gotify notification: {e}")

@app.route('/webhook', methods=['POST'])
def xray_webhook():
    data = request.json
    typed = data["type"]
    if typed == "web_statistic":
        return 'ok'
    vuln = data["data"]
    content = """## xray find new vuln

漏洞地址: {url}

插件: {plugin}

创建时间: {create_time}

""".format(url=vuln["detail"]["addr"], plugin=vuln["plugin"],
           create_time=str(datetime.datetime.fromtimestamp(vuln["create_time"] / 1000)))
    try:
        push_gotify(content)
    except Exception as e:
        logging.exception(e)

    return 'ok'

if __name__ == '__main__':
    app.run()

