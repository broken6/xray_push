from flask import Flask, request
import requests
import datetime
import logging

app = Flask(__name__)


def push_ftqq(content):
    resp = requests.post("https://sctapi.ftqq.com/SCT159684Tg85VBt6tqqqR0fEK6DhorT4Z.send",
                  data={"text": "xray vuln alarm", "desp": content})
    if resp.json()["data"]["errno"] != 0:
        raise ValueError("push ftqq failed, %s" % resp.text)

@app.route('/webhook', methods=['POST'])
def xray_webhook():
    data = request.json
    typed = data["type"]
    if typed == "web_statistic":
        return 'ok'
    vuln = data["data"]
    content = """## xray find new vuln

url: {url}

plugin: {plugin}

create_time: {create_time}

""".format(url=vuln["detail"]["addr"], plugin=vuln["plugin"],
           create_time=str(datetime.datetime.fromtimestamp(vuln["create_time"] / 1000)))
    try:
        push_ftqq(content)
    except Exception as e:
        logging.exception(e)
    return 'ok'


if __name__ == '__main__':
    app.run()

