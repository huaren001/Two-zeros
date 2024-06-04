import json
from flask import Flask, request
import api
import gpt
from cachetools import TTLCache

bnt_qq = 3476231673    #填你的副qq号
perfix = '[CQ:at,qq=' + str(bnt_qq) + ']'
messageCache = TTLCache(maxsize = 100, ttl = 20)

app = Flask(__name__)

'''黑名单'''
def isBlacklisted(uid):
    with open('./blacklist.txt','r') as f:
        blacklist = [int(line.strip()) for line in f.readlines()]
    return uid in blacklist

 
'''聊天结果保存'''
def saveData(nickName, question, result):
    newChat = {
        'promptTokens':result['promptTokens'],
        'completionTokens':result['completionTokens'],
        'totalTokens':result['totalTokens'],
        'chat':{
            'user':question,
            'bot':result['content']
        }
    }
    with open('tokens.json', 'r+') as f:
        data = json.load(f)
        if nickName in data:
            data[nickName].append(newChat)
        else:
            newUser = {nickName:[newChat]}
            data.update(newUser)
        f.seek(0)
        json.dump(data, f, ensure_ascii = False, indent = 4)

'''监听端口，实时获取QQ信息'''
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    if data['post_type'] == 'message':
        msgType = data['message_type']
        msgContent = data['message']
        msgID = data['message_id']
        uid = data['user_id']

        if msgID in messageCache:
            return 'OK'
        else:
            messageCache[msgID] = True

        if isBlacklisted(uid):
            answer = '你已被拉入黑名单'
            if msgType == 'private':
                api.sendPrivate(uid, answer)
            else:
                gid = data['group_id']
                api.sendGroup(uid, gid, answer)
            return 'OK'

        ''''非文字信息处理'''
        if msgContent.startswith('[CQ') or '请使用最新版手机QQ体验新功能' in msgContent:
            answer = '我只能处理文字消息'
            if msgContent.startswith(perfix):
                split_tmp = msgContent.split()
                msgContent = "".join(split_tmp[1:]) if len(split_tmp) > 1 else ""
                if msgContent.startswith('[CQ') or '请使用最新版手机QQ体验新功能' in msgContent:
                    gid = data['group_id']
                    api.sendGroup(uid,gid,answer)
                return 'OK'
            if msgType == 'private':
                api.sendPrivate(uid, answer)
                return 'OK'

        '''调用api'''
        answer = ''
        result = None
        try:
            result = gpt.chat(msgContent)
            answer = result['content']
        except Exception as e:
            answer = str(e)
        if msgType == 'group' and msgContent.startswith(perfix):
            gid = data['group_id']
            api.sendGroup(uid, gid, answer)
        if msgType == 'private':
            api.sendPrivate(uid, answer)

        if not result:
            return 'OK'

        nickName = data['sender']['nickname']
        saveData(nickName, msgContent, result)
        return 'OK'
    return 'OK'
 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5701)
