"""
Description  : 
Version      : 1.0.0
Author       : Xu Huasheng
Date         : 2023-02-03 11:17:14
LastEditTime : 2023-02-03 11:31:11
LastEditors  : aircas41-server-win xuhs@aircas.ac.cn
Copyright (c) 2023 AIRCAS. All rights reserved. 
"""
import os
import cv2
import eyed3
from eyed3.id3.frames import ImageFrame
from tqdm import tqdm

cover_path = r'cover2/jay.jpg'
mp3_path = r"G:\08.周杰伦"

img = cv2.imread(cover_path)
img = cv2.resize(img, (300, 300))
cv2.imwrite(cover_path, img)
for mp3 in tqdm(os.listdir(mp3_path)):
    audioFile: eyed3.AudioFile = eyed3.load(path=os.path.join(mp3_path, mp3))
    audioFile.tag.images.set(ImageFrame.FRONT_COVER, open(cover_path, 'rb').read(), 'image/' + 'jpg')
    audioFile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')