import requests
import random
import json
import re
from bs4 import BeautifulSoup

def get_users(text):
    try:
        data = json.loads(text)
        items = data.get('data').get('cards')
        for item in items:
            users = {}
            users["id"]=item.get('user').get('id')
            users["name"]=item.get('user').get('screen_name')
            users["des"]=item.get('desc1')
            yield users
    except:
        print("解析错误")
    finally:
        pass

def get_user_info(html):
    uer_info = {}
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            uer_info['containrid'] = data.get('data').get('tabsInfo').get('tabs')[1].get('containerid')
            uer_info['weibo_count']= data.get('data').get('userInfo').get('tatuses_count')
            uer_info['followers_count'] = data.get('data').get('userInfo').get('followers_count')
            uer_info['follow_count'] = data.get('data').get('userInfo').get('follow_count')
            return uer_info
    except:
        print("获取错误")

def get_user_weiboid(html):
    IdList=[]
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            items = data.get('data').get('cards')
            for item in items:
                if item and 'mblog' in item.keys():
                    id = item.get('mblog').get('id')
                    IdList.append(id)
                else:
                    continue
        return IdList
    except:
        print("error")

def get_weibo_content(html):
    html = BeautifulSoup(html,'lxml')
    pattern = re.compile('var \\$render_data = \\[(.*?)]\\[0]', re.S)
    result = re.search(pattern, html.text)
    if result:
        data = json.loads(result.group(1))
        if data and 'status' in data.keys():
            print(data.get('status').get('user').get('id'))
            print(data.get('status').get('created_at'))
            print(data.get('status').get('text'))
            print(data.get('status').get('reposts_count'))
            print(data.get('status').get('comments_count'))
            print(data.get('status').get('attitudes_count'))
            print(i.get('url') for i in data.get('status').get('pics'))

def main():
    session = requests.session()
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
        'Mobile/13B143 Safari/601.1]',
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) ',
        'Chrome/48.0.2564.23 Mobile Safari/537.36']

    headers = {
        'User_Agent': random.choice(user_agents),
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
        'Origin': 'https://passport.weibo.cn',
        'Host': 'passport.weibo.cn'
    }
    post_data = {
        'username': '',
        'password': '',
        'savestate': '1',
        'ec': '0',
        'pagerefer': 'https://m.weibo.cn/',
        'entry': 'mweibo'
    }
    login_url = 'https://passport.weibo.cn/sso/login'
    username = input('请输入用户名:\n')
    password = input('请输入密码：\n')
    post_data['username'] = username
    post_data['password'] = password
    r = session.post(login_url, data=post_data, headers=headers)
    if r.status_code != 200:
        raise Exception('模拟登陆失败')
    else:
        print("模拟登陆成功,当前登陆账号为：" + username)
    reponse = session.get('https://m.weibo.cn/api/container/getSecond?containerid=1005055236331671_-_FOLLOWERS')
    users = get_users(reponse.text)
    for user in users:
        try:
            id = user.get('id')
            url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+ str(id)
            reponse1= session.get(url)
            user_info = get_user_info(reponse1.text)
            url1 = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={0}&containerid={1}'.format(str(id),str(user_info['containrid']))
            print(url1)
            reponse2 = session.get(url1).text
            WeiboIdList = get_user_weiboid(reponse2)
            for li in WeiboIdList:
                url2 = 'https://m.weibo.cn/status/'+str(li)
                reponse3 = session.get(url2).text
                get_weibo_content(reponse3)
        except:
            continue


if __name__ == '__main__':
    main()