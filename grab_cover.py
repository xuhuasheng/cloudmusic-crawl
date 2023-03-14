"""
Description  : 
Version      : 1.0.0
Author       : Xu Huasheng
Date         : 2023-01-30 10:52:33
LastEditTime : 2023-02-03 18:47:07
LastEditors  : aircas41-server-win xuhs@aircas.ac.cn
Copyright (c) 2023 AIRCAS. All rights reserved. 
"""
import os
import eyed3
import cv2
import imghdr
import numpy as np
from eyed3.id3.frames import ImageFrame
from tqdm import tqdm
import requests
import json
import time
 
MP3_PATH = r"F:\musictest\04.女声推荐200首"
MP3_PATH_LST = [
    # r"F:\playlist\cl",
    r"./ywg",
]
WYY_OPENAPI_TEST_URL = "https://interface.music.163.com/api/growth/external/sandbox/request"

def grab_cover(idx, song_name):
    """通过歌名获取歌曲封面"""
    bizContentJson = json.dumps({
        "keyword": song_name,
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

    response = requests.request("POST", WYY_OPENAPI_TEST_URL, headers=headers, data=payload)
    res = response.json()
    res_lst = res['data']['responseData']['records']
    if len(res_lst) == 0:
        return None
    cover_img_url = res_lst[0].get('coverImgUrl', None)
    if cover_img_url is None:
        print(f"{idx}-{song_name}无封面url")
        return None
    cover_path = 'cover_img/' + f"{idx}-{song_name}.jpg"
    with open(cover_path,'wb') as f:
        img = requests.get(cover_img_url).content
        #url是img的url
        f.write(img)
    try:
        img = cv2.imread(cover_path)
    except:
        img = cv2.imdecode(np.fromfile(cover_path, dtype=np.uint8), -1)
    img = cv2.resize(img, (400, 400))
    cv2.imwrite(cover_path, img)
    return cover_path

 
if __name__ == '__main__':
    for lst in MP3_PATH_LST:
        mp3_file_lst = os.listdir(lst)
        for mp3file in tqdm(mp3_file_lst):
            if mp3file.split('.')[-1] != 'mp3':
                continue
            audioFile: eyed3.AudioFile = eyed3.load(path=os.path.join(lst, mp3file))
            idx = "0000"
            try:
                title = audioFile.tag.title
                cover_path = grab_cover(idx, title)
                if cover_path is None:
                    print(f"{mp3file}获取图片失败。")
                    continue
                img_type = imghdr.what(cover_path)
                audioFile.tag.images.set(ImageFrame.FRONT_COVER, open(cover_path, 'rb').read(), 'image/' + img_type)
                audioFile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')
            except:
                pass