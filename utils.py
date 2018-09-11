# -*- coding:utf-8 -*-
# Time: 2018/9/7 15:29
import locale

import os
import subprocess

locale.getpreferredencoding()


def create_folder(path):
    """根据提供的路径，path不存在则新建文件夹，也可以有子文件夹"""
    if not os.path.exists(path):
        os.makedirs(path)


def concatenate(path, dest='video'):
    """
    将给定路径下的视频进行合并，同时删除原本的视频
    :param path: 需要合并的视频所在文件夹名字，一般是视频名字
    :param dest: 合并之后的视频存放路径，默认为video文件夹
    :return:
    """
    with open('file.txt', 'a', encoding='utf-8') as f:
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] in ['.flv', '.mkv', '.mp4']:
                    video_path = os.path.join(root, file)
                    line = "file '{}'\n".format(video_path)
                    f.writelines(line)

    create_folder(dest)
    video_save_path = os.path.join(dest, path)

    # 合并视频
    if os.path.exists('file.txt'):
        ffmpeg_command = ["ffmpeg", "-f", "concat", "-safe", "0" , "-i", "file.txt", "-c", "copy", video_save_path+".mp4"]
        subprocess.run(ffmpeg_command)
        subprocess.run(["rm", "file.txt"])
        subprocess.run(["rm", "-r", path])
