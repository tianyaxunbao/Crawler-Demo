#!/usr/bin/env python
# encoding: utf-8
# @author: cc <chai_pengfei@163.com>，samuel


import requests
import re


class HuabanCrawler():
    """ 抓去花瓣网上的图片 """

    def __init__(self):
        """ 在当前文件夹下新建images文件夹存放抓取的图片 """
        self.homeUrl = "http://huaban.com/favorite/beauty/"
        self.images = []
 

    def __load_homePage(self):
        """ 加载主页面 """
        return requests.get(url = self.homeUrl).content

    def __make_ajax_url(self, No):
        """ 返回ajax请求的url """
        return self.homeUrl + "?i5p998kw&max=" + No + "&limit=20&wfl=1"

    def __load_more(self, maxNo):
        """ 刷新页面 """
        return requests.get(url = self.__make_ajax_url(maxNo)).content

    def __process_data(self, htmlPage):
        """ 从html页面中提取图片的信息 """
        prog = re.compile(r'app\.page\["pins"\].*')
        htmlPage = htmlPage.decode('utf-8')
        appPins = prog.findall(htmlPage)
        # 将js中的null定义为Python中的None
        null = None
        true = True
        if appPins == []:
            return None
        result = eval(appPins[0][19:-1])
        for i in result:
            info = {}
            info['id'] = str(i['pin_id'])
            info['url'] = "http://img.hb.aicdn.com/" + i["file"]["key"] + "_fw658"
            if 'image' == i["file"]["type"][:5]:
                info['type'] = i["file"]["type"][6:]
            else:
                info['type'] = 'NoName'
            self.images.append(info)

    def __save_image(self, imageName, content):
        """ 保存图片 """
        with open(imageName, 'wb') as fp:
            fp.write(content)
        file = drive.CreateFile({'title': imageName})
        file.SetContentFile(imageName)
        file.Upload() # Files.insert()
 
    def get_image_info(self, num=20):
        """ 得到图片信息 """
        self.__process_data(self.__load_homePage())
        for i in range((num-1)//20):
            self.__process_data(self.__load_more(self.images[-1]['id']))
        return self.images

    def down_images(self):
        """ 下载图片 """
        
        for key, image in enumerate(self.images):
            print ('download {0} ...'.format(key))
            try:
                req = requests.get(image["url"])
            except :
                print('error') 
            imageName = image["id"] + "." + image["type"]
            self.__save_image(imageName, req.content)



hc = HuabanCrawler()
hc.get_image_info(200)
hc.down_images()
