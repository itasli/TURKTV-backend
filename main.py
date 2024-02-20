import requests
import re
import json

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse

from fake_useragent import UserAgent

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/turkuvaz/{item_id}", response_class=FileResponse)
def turkuvaz(item_id: str):

    # item_id = ["atvhd", "a2tv", "ahaberhd", "aparahd", "asporhd", "atvavrupa", "minikagococuk", "minikago"]

    URL_LICENCE_KEY = "http://videotoken.tmgrup.com.tr/webtv/secure?url=http://trkvz-live.ercdn.net/%s/%s.m3u8"

    headers = {"User-Agent": UserAgent().random, 'Referer': 'https://www.atv.com.tr/canli-yayin'}

    resp = requests.get(URL_LICENCE_KEY % (item_id, item_id), headers=headers)
    video_url = re.compile('\"Url\":\"(.*?)\"').findall(resp.text)[0]

    return video_url


@app.get("/dogus/{item_id}", response_class=RedirectResponse)
def dogus(item_id: str):

    # item_id = ["eurostar"]

    URL_LIVE = {
        'eurostar': 'https://www.eurostartv.com.tr/canli-izle',
    }

    headers = {"User-Agent": UserAgent().random, 'Referer': URL_LIVE[item_id]}

    resp = requests.get(URL_LIVE[item_id], headers=headers)

    video_url = re.compile('var liveUrl = \'(.*?)\'').findall(resp.text)[0]

    return video_url


@app.get("/cinergroup/{item_id}", response_class=RedirectResponse)
def cinergroup(item_id: str):

    # item_id = ["showturk", "showmax"]

    URL_LIVE = {
        'showturk': 'https://www.showturk.com.tr/canli-yayin',
        'showmax': 'http://showmax.com.tr/canliyayin',
    }

    headers = {"User-Agent": UserAgent().random, 'Referer': URL_LIVE[item_id]}

    resp = requests.get(URL_LIVE[item_id], headers=headers)

    video_url = json.loads(re.compile(r'data-ht=\'(.*?)\'').findall(resp.text)[0])['ht_stream_m3u8']

    return video_url


@app.get("/tv8/{item_id}", response_class=RedirectResponse)
def tv8(item_id: str):

    # item_id = ["tv8"]

    URL_LIVE = "https://www.tv8.com.tr/canli-yayin"

    headers = {"User-Agent": UserAgent().random, 'Referer': URL_LIVE}

    resp = requests.get(URL_LIVE, headers=headers)

    video_url = re.compile('var videoUrl = \"(.*?)\"').findall(resp.text)[0]

    return video_url


@app.get("/kanal7/{item_id}", response_class=RedirectResponse)
def kanal7(item_id: str):

    # item_id = ["kanal7avrupa"]

    URL_LIVE = "https://www.kanal7avrupa.com/canli-izle"

    URL_DAILYMOTION_EMBED_2 = "https://www.dailymotion.com/player/metadata/video/%s"

    headers = {"User-Agent": UserAgent().random, 'Referer': URL_LIVE}

    resp = requests.get(URL_LIVE, headers=headers)

    video_token = re.compile('src=".*?dailymotion.*?=(.*?)"').findall(resp.text)[0]

    resp = requests.get(URL_DAILYMOTION_EMBED_2 % video_token, headers=headers)

    video_url = json.loads(resp.text)['qualities']['auto'][0]['url']

    return video_url


@app.get("/now/{item_id}", response_class=RedirectResponse)
def now(item_id: str):

    # item_id = ["now"]

    URL_LIVE = "https://www.nowtv.com.tr/canli-yayin"

    headers = {"User-Agent": UserAgent().random, 'Referer': URL_LIVE}

    resp = requests.get(URL_LIVE, headers=headers)

    video_url = re.compile('daiUrl : \'(.*?)\'').findall(resp.text)[0]

    return video_url
