"""
Description  : 
Version      : 1.0.0
Author       : Xu Huasheng
Date         : 2023-02-02 17:41:51
LastEditTime : 2023-02-02 18:12:08
LastEditors  : aircas41-server-win xuhs@aircas.ac.cn
Copyright (c) 2023 AIRCAS. All rights reserved. 
"""
from Crypto.Cipher import AES
import base64
import json
import requests

# 常量
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Referer':
    'https://music.163.com/',
    'Content-Type':
    'application/x-www-form-urlencoded',
}
post_url = 'https://music.163.com/weapi/song/enhance/player/url'
content = {"ids": "", "br": 128000, "csrf_token": ""}
key1 = b'0CoJUm6Qyw8W8jud'
key2 = b'ryPnuAVT5RtiIWNi'
encSecKey = 'a71973af53caae445b554150da52e75ba5687609d28013aacea03e9ef07169560f156ca76be9ac8df7bb204e05b864756aa3dd2274a65d5be964f118f6d075006695059e10cdcc806306e9a5f2f36f5bf0379f511cd13a600a6cc7031c814583863ea84d3373dea69f74354cd2dc3af61d58eeb43b1de06f588ef361ebc1eed6'

# 加密
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
encrypt_token = lambda key, content: AES.new(key=key, mode=AES.MODE_CBC, IV=b'0102030405060708').encrypt(pad(content).encode())


# 接口
def music_interface(song_id):
    content["ids"] = "[{}]".format(song_id)
    str_content = json.dumps(content)
    tmp = base64.b64encode(encrypt_token(key1, str_content)).decode()
    params = base64.b64encode(encrypt_token(key2, tmp)).decode()
    post_data = {
        'params': params,
        'encSecKey': encSecKey,
    }
    resp = requests.post(url=post_url, headers=headers, data=post_data)
    js = json.loads(resp.content)
    song_url = js['data'][0]['url']
    return song_url


if __name__ == '__main__':
    song_url = music_interface('1913421961')
    print(song_url)