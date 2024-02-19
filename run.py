import argparse
import os
import logging
import platform
import requests
from src.Utils import logout
from pathlib import Path
import sys
from cli import *
from src.plots import generate_word,generate_histogram,read_xml_dm
from Comic import manga
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))
def setEnvironmentVariable(name, value):
    '''Set an environment variable in both current and permanent environment '''
    os.environ[name] = value
    # os.system('set '  + name + ' = ' + value)       # for this shell
    # os.system('setx ' + name + ' "'  + value + '"') # for the permanent user environment
def get_system():
    system_name = platform.system().lower()
    logout(f"系统类型:{system_name}")
    if system_name == 'windows':
        setEnvironmentVariable("ffmpeg",os.path.abspath("drive/ffmpeg/x64/win/bin/ffmpeg.exe"))
    elif system_name == 'linux':
        setEnvironmentVariable("ffmpeg",os.path.abspath("drive/ffmpeg/x64/linux/bin/ffmpeg"))
    elif system_name == 'darwin':
        setEnvironmentVariable("ffmpeg",os.path.abspath("drive/ffmpeg/x64/mac/ffmpeg"))
    else:
        os.system("pip install pyffmpeg")
def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', '-l',action='store_true', help='login bilibili')
    parser.add_argument('--choose', '-c', type=str, default="", help='manga or video')
    parser.add_argument('--show', action='store_true', help='show config')
    parser.add_argument('--path', '-P', type=str, default="cache",help='bilibili download video save path')
    #################################  VIDEO  ####################################################
    parser.add_argument('--multi_threaded', '-mt', action='store_true', help='open multi-threaded download')
    parser.add_argument('--proxy', '-p', type=str, default="", help='proxy url and prot (127.0.0.1:7890")')
    # parser.add_argument('--url', '-u', type=str, default="https://www.bilibili.com/video/BV17p4y1N7sD/", help='bilibili use url or video url')
    parser.add_argument('--id','-i',type=str,default="BV17p4y1N7sD",help='video: bvid or epid')
    parser.add_argument('--dm',action='store_true',help='download video bilibili dm')
    #################################  MANHUA  ####################################################
    parser.add_argument('--comic_id','-cid',type=int,default=28201,help='Comic id (url:https://manga.bilibili.com/detail/mc28201 -> id:28201)')
    #################################  DRAW  ####################################################
    parser.add_argument('--read','-r',  type=str, default=ROOT / "cache/鸿蒙.xml", help='Read xml path')
    parser.add_argument('--draw', '-d',action='store_true',help='dm xml draw')

    return parser.parse_known_args()[0] if known else parser.parse_args()
def main(opt):
    logging.basicConfig(level=logging.INFO, filename="cache/run.log", encoding='utf-8')
    id = opt.id
    co = init()
    show_config(co)
    if opt.login:
        co.login_update_headers()
    if opt.show:
        show_config(co)
    if opt.draw:
        words = read_xml_dm(opt.read)
        generate_histogram(words)
        generate_word(words)
    if opt.proxy != "":
        try:
            proxy = {
                'http': opt.proxy
            }

            if requests.get("https://baidu.com", proxies=proxy).text != 200:
                logout(f"http代理{opt.proxy}正常")
        except:
            logout(f"http代理{opt.proxy}无法使用", "error")
    if opt.choose == "video":
        if opt.dm:
            co.set_none_headers_config(dm=True)
        else:
            co.set_none_headers_config(dm=False)
        if opt.multi_threaded:
            logout("开启多线程下载")
        if id[:2] == "BV":
            bvid = id
            cid_group = co.get_cid(bvid)
            # 单p直接下载
            if (len(cid_group) == 1):
                p_download(co, bvid, cid_group)
            # 多p下载
            else:
                np_download(co, bvid, cid_group)
        # ep_id
        else:
            spid = id
            co.download_epid_video(spid)

        pass
    elif opt.choose == "manga":
        id = opt.comic_id
        manga(cookie=co.get_config()['headers']['cookies']).download_manga_all(id)
    # if
# def checkcore()
# def run(**kwargs):
#     opt = parse_opt(True)
#     for k, v in kwargs.items():
#         setattr(opt, k, v)
#     main(opt)
#     return opt
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,filename="cache/run.log",encoding='utf-8')
    # os.environ['path'] = f'{os.path.abspath("encoding/video/x64/win/bin")}'
    get_system()
    opt = parse_opt(True)
    main(opt)