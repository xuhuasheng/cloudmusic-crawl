"""
Description  : 
Version      : 1.0.0
Author       : Xu Huasheng
Date         : 2023-01-29 17:05:17
LastEditTime : 2023-01-30 09:54:03
LastEditors  : xuhuasheng xu_watson@163.com
Copyright (c) 2023 AIRCAS. All rights reserved. 
"""
#!/usr/bin/env python
# encoding: utf-8

import os
import eyed3
import imghdr
from eyed3.id3.frames import ImageFrame
from tqdm import tqdm
 
MP3_PATH = r"G:\musictest\03.粤语热歌200首"


def Mp3(mp3_path):
    """
    mp3文件修改属性
    :param mp3_path:
    :param img_path:
    :return:
    """
    audioFile: eyed3.AudioFile = eyed3.load(path=mp3_path)
    # audioFile.tag.artist = u"五条人"
    # audioFile.tag.title = u"世界的理想"
    # audioFile.tag.album = u"乐队的夏天"
    audioFile.tag.artist = artist
    audioFile.tag.title = title
    # audioFile.tag.album = album
    # img_type = imghdr.what(img_path)
    # audioFile.tag.images.set(ImageFrame.FRONT_COVER, open(img_path, 'rb').read(), 'image/' + img_type)
    # audioFile.tag.save()   
    audioFile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')
 
if __name__ == '__main__':
    mp3_file_lst = os.listdir(MP3_PATH)
    for mp3file in tqdm(mp3_file_lst):
        if mp3file.split('.')[-1] != 'mp3':
            continue
        try:
            audioFile: eyed3.AudioFile = eyed3.load(path=os.path.join(MP3_PATH, mp3file))
        except Exception as e:
            print(f"{mp3file}====={e}:")
        try:
            artist_title = mp3file.split('.')[-2].split('-')
            artist = artist_title[1].strip()
            title = artist_title[0].strip()
        except:
            print(mp3file)
            artist = "未知"
            title = artist_title[0].strip()
            # continue
        if title in ("刘德华", "林子祥", "谭咏麟", "卢冠廷", "王菲", "许冠杰", "张国荣", "郑少秋", "张智霖", "郑欣宜", "郑秀文",
                    "钟嘉欣", "周慧敏", "周华健_齐豫", "BEYOND", "Beyond", "张智霖_许秋怡", "李克勤"):
            artist, title = title, artist
        if title == "邓紫棋":
            artist = "邓紫棋"
            title = mp3file.split('.')[1].split('-')[0].strip()
        audioFile.tag.artist = artist
        audioFile.tag.title = title
        audioFile.tag.album = title
        audioFile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')
        