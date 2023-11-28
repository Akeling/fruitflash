from selenium import webdriver
import time
import os
import requests
from selenium.webdriver.common.by import By
# 搜索关键词
keyword = '新鲜的苹果'
url = 'https://www.google.com.hk/search?q=' + keyword + '&tbm=isch'


class Crawler_google_images:
    # 初始化
    def __init__(self):
        self.url = url

    # 获得Firefox驱动，并访问url
    def init_browser(self):
        browser = webdriver.Chrome()
        # 访问url
        browser.get(self.url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        browser.maximize_window()
        return browser

    # 下载图片
    def download_images(self, browser, round=2):
        picpath = './photo/{}/'.format(keyword)
        if not os.path.exists(picpath):
            os.makedirs(picpath)
        count = 0
        pos = 0
        for i in range(round):
            img_url_dic = []
            pos += 500
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(3)
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            wait = WebDriverWait(browser, 10)
            img_elements = browser.find_elements(by=By.TAG_NAME, value='img')
            for img_element in img_elements:
                img_url = img_element.get_attribute('src')
                if isinstance(img_url, str) and len(img_url) <= 200 and 'images' in img_url:
                    if img_url not in img_url_dic:
                        try:
                            img_url_dic.append(img_url)
                            filename = picpath + str(count) + ".jpg"
                            r = requests.get(img_url)
                            r.raise_for_status()  # 抛出HTTPError异常
                            with open(filename, 'wb') as f:
                                f.write(r.content)
                            count += 1
                            print('Downloaded ' + str(count) + 'st image')
                            time.sleep(0.5)
                        except requests.exceptions.RequestException as e:
                            print(f"Request Exception for image {count}: {e}")
                            # 记录请求异常到日志文件
                            with open('error_log.txt', 'a') as log_file:
                                log_file.write(f"Request Exception for image {count}: {e}\n")
                        except IOError as e:
                            print(f"IO Error for image {count}: {e}")
                            # 记录IO异常到日志文件
                            with open('error_log.txt', 'a') as log_file:
                                log_file.write(f"IO Error for image {count}: {e}\n")
                        except Exception as e:
                            print(f"An error occurred for image {count}: {e}")
                            # 记录其他异常到日志文件
                            with open('error_log.txt', 'a') as log_file:
                                log_file.write(f"An error occurred for image {count}: {e}\n")

    def run(self):
        self.__init__()
        browser = self.init_browser()
        # 可以修改爬取的页面数，基本10页是100多张图片
        self.download_images(browser, 3)
        browser.close()
        print("爬取完成")


if __name__ == '__main__':
    craw = Crawler_google_images()
    craw.run()

