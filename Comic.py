import os
import time
import logging
import requests
import json
from pprint import pprint
from src.index_decode import decode_index_data
from src.Utils import logout
import csv

headers_cdn = {
                'Host': 'manga.hdslb.com',
                'Origin': 'https://manga.bilibili.com',
            }
class manga:
    def __init__(self,download_path="./manhua",cookie=""):
        '''
        init
        Args:
            download_path: 下载存放路径
            cookie: cookie
        '''
        if download_path =="":
            download_path = "./manhua"
        self.download_path = download_path
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Type": "application/json;charset=UTF-8",
            "origin": "https://manga.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            "cookie": ""}
        self.headers['cookie'] = str(cookie)


    def download_manga_all(self,comic_id: int):
        url = "https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web"
        # self.headers.update({'Referer' : 'https://manga.bilibili.com/detail/' + comic_id})
        print(self.headers)
        res = requests.post(url,json.dumps({
                                "comic_id": comic_id
                            }),headers=self.headers)
        print(res)
        data = json.loads(res.text)['data']
        comic_title = data['title']
        root_path = os.path.join(self.download_path, comic_title)
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        for ep in data['ep_list']:
            if not ep['is_locked']:
                print('downloading ep:', ep['short_title'], ep['title'])
                try:
                    pppp = int(ep['short_title'])
                    if pppp>=58:
                        # time.sleep(0.1)
                        continue
                except:
                    pass
                self.download_manga_episode(ep['id'], root_path)
                pass
            pass
        pass


    def download_manga_episode(self,episode_id: int, root_path: str):
        res = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web',
                            json.dumps({
                                "id": episode_id
                            }), headers=self.headers)
        data = json.loads(res.text)
        # comic_title = data['data']['comic_title']
        short_title = data['data']['short_title']
        # title = comic_title + '_' + short_title + '_' + data['data']['title']
        title = short_title + '_' + data['data']['title']
        title = title.replace('?','？')
        comic_id = data['data']['comic_id']
        print('正在下载：', title)
        logout(f"正在下载：, {title}")
        # 获取索引文件cdn位置
        res = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web',
                            json.dumps({
                                "ep_id": episode_id
                            }), headers=self.headers)
        data = json.loads(res.text)
        index_url = 'https://manga.hdslb.com' + data['data']['path']
        print('获取索引文件cdn位置:', index_url)
        # 获取索引文件
        res = requests.get(index_url)
        # 解析索引文件
        pics = decode_index_data(comic_id

                                 , episode_id, res.content)
        # print(pics)
        print(title, type(title))
        ep_path = os.path.join(root_path, title)
        if not os.path.exists(ep_path):
            os.mkdir(ep_path)
        for i, e in enumerate(pics):
            url = self.get_image_url(e)
            print(i, e)
            res = requests.get(url)
            try:
                with open(os.path.join(ep_path, str(i) + '.jpg'), 'wb+') as f:
                    f.write(res.content)
                    pass
                if i % 4 == 0 and i != 0:
                    time.sleep(2)
                pass
            except:
                logout(f"{i}--{e} 文件写入失败",config="error")
                # with open('./ERROR.txt')

            pass
        pass


    def get_image_url(self,img_url):
        # 获取图片token
        res = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web',
                            json.dumps({
                                "urls": json.dumps([img_url])
                            }), headers=self.headers)
        data = json.loads(res.text)['data'][0]
        url = data['url'] + '?token=' + data['token']
        return url
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="run.log", encoding='utf-8')
    maga = [#[27356,27375,28937]
            #27596
            27549,29391,29036,28078]
            # 29695,28421,27646,28535,27355,29724,29445,
            # 26991,29696,27200,27888,27386,28612,26746,
            # 30788,28579]
    a = manga(cookie="buvid3=19257883-5509-3088-AD84-94FB980E76AE76570infoc; b_nut=1702352476; i-wanna-go-back=-1; b_ut=7; b_lsid=5106B44B9_18C5C1D5E19; _uuid=41010DABDE-18A3-C387-55F5-D415BD133BC177729infoc; enable_web_push=DISABLE; home_feed_column=5; buvid4=FE5D69EE-D57F-8F0E-4508-0C6C224165D078852-023121203-; buvid_fp=ae5b04c12707bc7d7f7e3f1b991e5dca; header_theme_version=CLOSE; browser_resolution=1707-950; sid=77jpsdkr; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI2MTE3MTgsImlhdCI6MTcwMjM1MjQ1OCwicGx0IjotMX0.RfLXhmZu5qqPNGhzYGspVjv96K1bpc2YU41B_24tCA8; bili_ticket_expires=1702611658; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; is-2022-channel=1; rpdid=|(JJmlm|kRl~0J'u~|kJlkY)); DedeUserID=179137115; DedeUserID__ckMd5=a13204249f40e491; SESSDATA=a69bf0db%2C1717906786%2Cdba0f*c1; bili_jct=ea7f829576621317158db976168ab209; fingerprint=ae5b04c12707bc7d7f7e3f1b991e5dca; innersign=0; bp_video_offset_179137115=874106590159962153; bsource=search_bing")
    a.download_manga_all(28201)
    # for download in maga:
    #     a.download_manga_all(download)
    #     # download_manga_episode(448369, os.path.join(download_path, '辉夜大小姐想让我告白 ~天才们的恋爱头脑战~'))
    #     # get_image_url('/bfs/manga/f311955085404cab705e881d0a81204098967c1e.jpg')
    #     pass



