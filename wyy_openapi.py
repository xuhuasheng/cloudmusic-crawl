import time
import requests
import json

url = "https://interface.music.163.com/api/growth/external/sandbox/request"

bizContentJson = json.dumps({
        "keyword": "成都",
        "limit": "5",
        "offset": "0"
})

payload = json.dumps({
   "appId": "a301020000000000ac22dc8fa20e3795",
   "accessToken": "y8f3b107ed962c79ade975991c3cde622c77459eb28d2b14af",
   "timestamp": round(time.time() * 1000),
   "url": "/openapi/music/basic/search/song/get/v2",
   "bizContentJson": bizContentJson
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
   'Content-Type': 'application/json',
   'Accept': '*/*',
   'Host': 'interface.music.163.com',
   'Connection': 'keep-alive',
   'Cookie': 'NMTID=00O2KX_IY2cKKR16UKKi6A9SMBbdnMAAAGGBvIEPw'
}

response = requests.request("POST", url, headers=headers, data=payload)
res = response.json()
res_lst = res['data']['responseData']['records']
cover_img_url = res_lst[0]['coverImgUrl']

with open('test.jpg','wb') as f:
    img = requests.get(cover_img_url).content
    #url是img的url
    f.write(img)

print(response.json())