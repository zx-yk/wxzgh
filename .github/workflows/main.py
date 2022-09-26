import requests
import json
from datetime import datetime

def httpGet(url, params):
    r = requests.get(url, params)
    return json.loads(r.content)

def httpPost(url, params):
    r = requests.post(url, params)
    return json.loads(r.content)

# 获取微信token
def getAccessToken(appId, appSecret):
    params = {
        'grant_type': 'client_credential',
        'appid': appId,
        'secret': appSecret
    }
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    return httpGet(url, params)

#获取星座运势
def getStar(star, key):
    url = 'http://web.juhe.cn/constellation/getAll'
    params = {
        'key': key,
        'consName': star,
        'type': 'today',
        'extensions': 'base',
        'output': 'JSON',
    }
    return httpGet(url, params)

# 获取天气
def getWeather(abCode, key):
    url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    params = {
        'key': key,
        'city': abCode,
        'extensions': 'base',
        'output': 'JSON',
    }
    return httpGet(url, params)

# 获取一句情话
def getHua():
    url = 'https://yuxinghe.top/api/love.php'
    hua = httpGet(url, {'type': 'json'})
    return hua['ishan']

# 获取生日倒计时
def getBirthDays(birthDay):
    birthDay = datetime.strptime(birthDay, '%Y-%m-%d')
    interval = birthDay - datetime.now()
    return interval.days

# 获取在一起天数
def getTogetherDays(togetHerDay):
    togetHerDay = datetime.strptime(togetHerDay, '%Y-%m-%d')
    interval = datetime.now() - togetHerDay
    return interval.days

# 发送模版消息
def sendTemplateMessage(content, accessToken):
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + accessToken
    return httpPost(url, content)

# 获取星期
def getWeek():
    w = datetime.now().strftime('%w')
    data = {
        0: '星期天',
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六'
    }
    return data[int(w)]

if __name__ == '__main__':
    # 微信公众号的appId和appSecret
    appId = 'wx0ba8ab3d5dd8ec0d'
    appSecret = '4b3d6cbf754ba8e57c3c63a8e4f8e294'
    # 要发送人的openId列表
    openIdList = ['ofngy51wcjExzAiFlLCLOrTYIiG8','ofngy54YIdPePMHO7MWqBN3krPBQ','ofngy591lXjfEmr89FdjxS12ZzCI']
    # openIdList = ['ofngy51wcjExzAiFlLCLOrTYIiG8']
    # 模版Id
    templateId = 'EC4ThFNAtVf1bzCKi30TW92heI1Cibgn0-v626lPZsM'
    # 高德天气API key
    gaoDeKey = '5d8267e22864cb73024e3303ee55b192'
    # 聚合API key
    juheKey = 'cebfef27c5ced729984c6701d21c48e4'
    # 所在地点abCode（高德后台可以获取）
    abCode = '420115'
    # 最近一次生日的日期
    birthDay = '2023-05-21'
    # 在一起的时间
    togetHerDay = '2020-01-13'
    #星座
    star='双子座'

    accessTokenInfo = getAccessToken(appId, appSecret)
    accessToken = accessTokenInfo['access_token']
    weatherInfo = getWeather(abCode, gaoDeKey)
    weather = weatherInfo['lives'][0]
    starInfo = getStar(star, juheKey)
    #print(starInfo['money'])
    hua = getHua()
    birthDays = getBirthDays(birthDay)
    togetHerDays = getTogetherDays(togetHerDay)
    week = getWeek()
    #print(weatherInfo)
    #print(weather)
    for i in range(len(openIdList)):
        data = {
            'touser': openIdList[i],
            'template_id': templateId,
            'topcolor' : '#FF0000',
            'data': {
                'date': {
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'color': '#FB8953'
                },
                'province': {
                    'value': weather['province'],
                    'color': '#4d79ff'
                },
                'weather': {
                    'value': weather['weather'],
                    'color': '#00FFFF'
                },
                'city': {
                    'value': weather['city'],
                    'color': '#4d79ff'
                },
                # 'daytemp': {
                #     'value': weather['daytemp'],
                #     'color': '#54DA46'
                # },
                # 'nighttemp': {
                #     'value': weather['nighttemp'],
                #     'color': '#54DA46'
                # },
                'temperature': {
                    'value': weather['temperature']+'℃',
                    'color': '#54DA46'
                },
                'humidity': {
                    'value': weather['humidity']+'%',
                    'color': '#918597'
                },
                'winddirection': {
                    'value': weather['winddirection']+'风',
                    'color': '#bed742'
                },
                'windpower': {
                    'value': weather['windpower']+'级',
                    'color': '#dea32c'
                },
                'togetherDays': {
                    'value': togetHerDays+1,
                    'color': '#ff4dff'
                },
                'birthDays': {
                    'value': birthDays,
                    'color': '#ff4dff'
                },
                'week': {
                    'value': week,
                    'color': '#905ADA'
                },
                'star': {
                    'value': starInfo['money'],
                    'color': '#ed1941'
                },
                'summary': {
                    'value': starInfo['summary'],
                    'color': '#deab8a'
                },
                'hua': {
                    'value': hua,
                    'color': '#FFCFD7'
                }
            }
        }
        params = json.dumps(data)

        print(sendTemplateMessage(params, accessToken))


