import json
from requests_oauthlib import OAuth1Session
from dateutil.parser import parse as dateutil_parser
import datetime
from dateutil.relativedelta import relativedelta

#APIキーの設置
CONSUMER_KEY =  'XXXX'
CONSUMER_SECRET = 'XXXX'
ACCESS_TOKEN = 'XXXX'
ACCESS_SECRET = 'XXXX'

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
url = "https://api.twitter.com/1.1/search/tweets.json"

#各ガチャの最高レアの期待値（100円あたり）
gacha_percent_dic = {"ウマ娘":0.865,"バンドリ":0.882,"原神":0.186,"プロセカ":0.952,"パズドラ":0.976}


def kitaichi(game_name):
    tweets = []
    
    #パラメーター取得
    gacha_percent = gacha_percent_dic[game_name]
    keyword = game_name + " ガチャ" + " 当たった"
    today = datetime.datetime.today()
    since_dt = today - relativedelta(months=1)
    since_dt = str(one_month_ago).split(".")[0]
    since_dt = dateutil_parser(since_dt+"+00:00")
    
    params = {'q' : keyword, 'count' : 100}
    req = twitter.get(url, params = params)

    if req.status_code == 200:
        search_timeline = json.loads(req.text)
        for tweet in search_timeline['statuses']:
            dt = dateutil_parser(tweet.get("created_at")) + datetime.timedelta(hours=9)
            if dt >= since_dt: 
                tweets.append(tweet['id'])
    else:
        print("ERROR: %d" % req.status_code)
        
    kitaichi = len(tweets) * gacha_percent
    return kitaichi
