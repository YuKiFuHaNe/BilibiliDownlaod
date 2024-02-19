import logging
import datetime

# WEBDRIVE_PATH = "../drive/chromedriver.exe"
WEBDRIVE_PATH = "drive/msedgedriver.exe"
PIL_MASK_PATH = 'image/bg.jpg'
CACHE_PATH = 'cache'
FONTS_PATH = 'fonts'
def logout(*args,config="info".lower()):
    '''
    日志输出
    :param logdata_ch: 中文
    :param logdata_en: 英文
    :param config: 日志等级 info warning error
    '''
    log_data = ""
    print(args)
    for i in args:
        print(i)
        i = str(i)
        log_data = r"{:<50s} |  ".format(i)
        print(log_data)
    log_data += "[{}]".format(datetime.datetime.now())
    if config == "info":
        logging.info(log_data)
    elif config == "warning":
        logging.warning(log_data)
    elif config == "error":
        logging.error(log_data)
    else:
        logging.error(f"%-50s | %-50s |  [%-20s]", "log类型指定错误", "log type specification error",datetime.datetime.now())
