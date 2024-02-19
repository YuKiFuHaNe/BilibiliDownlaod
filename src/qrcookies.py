import requests
import qrcode
import re
from OCR.ocr import Chaojiying_Client
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from msedge.selenium_tools import Edge,EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from src.Utils import WEBDRIVE_PATH,logout,CACHE_PATH
import time
import random
import logging
import cv2
import os
def selenium_get_cookies_qr():
    '''
    Returns:cookies
    '''
    cookies = None
    options = EdgeOptions()
    options.use_chromium = True
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    options.add_argument('--disable-blink-features=AutomationControlled')  # 允许自动化控制
    # logout("启动Edge Webdrive ,请手动登录,完成输入yes | Y 后会车!")
    logout("启动Edge Webdrive")
    drive = Edge(WEBDRIVE_PATH, options=options)
    url = "https://space.bilibili.com/"
    drive.get(url)
    time.sleep(2)

    # while(1):
    #     _ = input()
    #     if _.lower() == "y" or "yes":
    #         try:
    #             cookies = drive.get_cookie()
    #             print(cookies)
    #             break
    #         except:
    #             logout("cookies获取失败----请检查后再次尝试！",config="error")
    #             pass
    drive.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/input').send_keys("915228208@qqq.com")
    drive.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/input').send_keys("915228208@qqq.com")
    drive.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]').click()
    time.sleep(2)
    verify_img_element = drive.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]')
    logout("验证图像获取成功！")
    chaojiying = Chaojiying_Client('YuKiFuHaNe', '510507100703lL', '938488')
    dic = chaojiying.PostPic(verify_img_element.screenshot_as_png,9004)
    # 返回示例x1,y1|x2,y2|x3,y3
    result = dic['pic_str']
    rs_list = result.split("|")
    logout("正在自动化填写验证码，请勿控制鼠标！")
    for rs in rs_list:
        p_temp = rs.split(',')
        x = int(p_temp[0])
        y = int(p_temp[1])
        time.sleep(random.uniform(0.1,1.5))
        ActionChains(drive).move_to_element_with_offset(verify_img_element, x,
                                                      y).click().perform()  # 找到某个节点，在这个节点的左上角做顶点坐标，进行一个offset的偏移
    logout("验证码填写完成,正在点击登录!")
    drive.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/div/div[3]/a').click()
    time.sleep(3)
    cookies = drive.get_cookies()
    logout("关闭Webdrive驱动")
    drive.close()
    return cookies

def get_cookies_qr(headers):
    print("准备扫码登录获取cookies")
    url="https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
    response = requests.get(url, headers=headers)
    qrcode_key=response.json()['data']['qrcode_key']
    qr_url=response.json()['data']['url']
    img=qrcode.make(qr_url)
    img.save(os.path.join(CACHE_PATH,'qrcode.png'))
    img_ = cv2.imread(os.path.join(CACHE_PATH,'qrcode.png'))
    print("扫码成功登入后请按q键并回车进行下一步")
    while(True):
        if cv2.waitKey(1) & 0xff ==ord('q'):
            break
        cv2.imshow("BiliBili QRCode",img_)
    pass_url="https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key="+qrcode_key

    cv2.destroyAllWindows()
    response = requests.get(pass_url, headers=headers)
    res=response.json()['data']['url']
    match = re.search(r'SESSDATA(.+?)&', res)
    ans=None
    if match:
        ans=match.group()
    return ans
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,filename="run.log",encoding='utf-8')
    selenium_get_cookies_qr()