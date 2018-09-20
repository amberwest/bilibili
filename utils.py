# -*- coding:utf-8 -*-
# Time: 2018/9/7 15:29
import locale

import os
import subprocess

import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from setting import BASE_DIR

locale.getpreferredencoding()

base_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

def request_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """遇到网络问题最多重试三次"""
    session = session or requests.session()
    retry = Retry(total=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)

    adapter = HTTPAdapter(max_retries=retry)

    session.mount('http', adapter=adapter)
    session.mount('https', adapter=adapter)

    return session

def get_page(url, method='get', params=None, options={}):
    """请求页面"""
    headers = dict(base_header, **options)
    session = request_retry_session()
    print('正在抓取：', url)

    try:
        if method == 'get':
            response = session.get(url, params=params, headers=headers)
        elif method == 'post':
            response = session.post(url, data=params, headers=headers)
        if response.status_code == 200:
            return response
    except Exception as e:
        print('网页请求失败: ', e)
        return None

def parse_url(url):
    """返回链接中的视频类型和id"""
    # url = 'https://www.bilibili.com/video/av28191704/?spm_id_from=333.788.videocard.0'
    reg = re.compile('.*?\/([a-z]{2})?(\d+)\/?.*?')
    res = reg.findall(url)
    if res:
        try:
            return res[0][0], res[0][1]
        except:
            return '', ''.join(res)
    else:
        return None, None

def create_folder(path):
    """根据提供的路径，path不存在则新建文件夹，也可以有子文件夹"""
    if not os.path.exists(path):
        os.makedirs(path)

def concatenate(path, dest):
    """
    将给定路径下的视频进行合并，同时删除原本的视频
    :param path: 需要合并的视频所在文件夹名字，一般是视频名字
    :param dest: 合并之后的视频存放路径，默认为video文件夹
    :return:
    """
    # 保存分段视频的临时文件
    new_path = path + '.txt'
    with open(new_path, 'a', encoding='utf-8') as f:
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] in ['.flv', '.mkv', '.mp4']:
                    video_path = os.path.join(root, file)
                    line = "file '{}'\n".format(video_path)
                    f.writelines(line)

    # 合并视频
    if os.path.exists(new_path):
        create_folder(dest)
        video_save_path = os.path.normpath(os.path.join(BASE_DIR, dest, path))
        try:
            print('开始合并视频...')
            print(path)
            ffmpeg_command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "file.txt", "-c", "copy",
                              video_save_path + ".mp4"]
            subprocess.run(ffmpeg_command)
            subprocess.run(["rm", "file.txt"])
            subprocess.run(["rm", "-r", path])
            print('视频合并完成！')
        except Exception as e:
            print('视频合并失败')
            print(e)
