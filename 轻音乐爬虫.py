import requests
from selenium import webdriver
from lxml import etree
import time


class Spider(object):

    def __init__(self):

        self.begin = begin

        self.end = end

        self.song_name = []

        self.song_id = []

        self.file = 1

        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        " (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}

    def b_spider(self):
        """构建每一页榜单的页面URL"""

        for i in range(self.begin-1, self.end):

            url = "http://www.htqyy.com/top/musicList/hot?pageIndex=" + str(i) + "&pageSize=20"

            self.load_page(url)

    def load_page(self, url):
        """用xpath提取歌曲名和ID"""

        response = requests.get(url, headers=self.header).text

        html = etree.HTML(response)

        # 歌曲名
        a = html.xpath(r'//li//span[@class="title"]/a')

        self.song_name.extend(a)

        # ID号
        b = html.xpath(r'//li//span//a/@sid')

        self.song_id.extend(b)

        self.music_spider()

    def music_spider(self):
        """构建每一首歌的URL"""

        for j in range(0, len(self.song_id)):

            m_url = "http://www.htqyy.com/play/%s" % (self.song_id[j])

            self.web_spider(m_url)

    def web_spider(self, m_url):
        """用selenium解析JS渲染过的每一首歌的URL"""

        driver = webdriver.Chrome()  # 创建一个浏览器驱动对象

        driver.get(m_url)      # 然后将URL传给这个驱动

        data = driver.page_source  # 然后用这个方法执行

        driver.close()  # 关闭浏览器驱动

        self.full_spider(data)

    def full_spider(self, data):
        """解析后再用xpath提取可下载歌曲的URL"""

        data2 = etree.HTML(data)

        mp3_url = data2.xpath(r"//div[@id='jquery_jplayer_1']/audio[@id='jp_audio_0']/@src")

        for link in mp3_url:

            self.write_mp3(link)

    def write_mp3(self, link):
        """通过MP3链接，爬取歌曲并保存到本地"""

        print("正在爬取第%d首歌曲==>>%s" % (self.file, (self.song_name[0]).text))
        mp3 = requests.get(link, headers=self.header).content
        file = open(r"C:\Users\autof\Desktop\轻音乐\\%s.mp3" % str((self.song_name[0]).text), "wb")
        file.write(mp3)
        file.close()
        self.file += 1
        self.song_name.pop(0)

        time.sleep(1)


if __name__ == "__main__":
    """执行的主程序"""

    begin = int(input("请输入要下载的开始页："))

    end = int(input("请输入要下载的结束页："))

    my_spider = Spider()

    my_spider.b_spider()

