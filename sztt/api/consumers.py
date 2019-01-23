from channels import Group
import json


def ws_connect(message):
    Group('users').add(message.reply_channel)
    message.reply_channel.send({
        'text': json.dumps({
            'msg': "你好",
            'talk': False
        })
    })


def ws_disconnect(message):
    Group('users').discard(message.reply_channel)


def ws_receive(message):
    data = json.loads(message['text'])
    message.reply_channel.send({
        'text': json.dumps({
            'msg': f"{data['text']}",
            'talk': True
        })
    })
