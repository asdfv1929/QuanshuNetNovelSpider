'''
File Name:    OneNovelContents
Description:  针对全书小说网中某一小说进行各章节内容爬取
Author:       jwj
Date:         2018/1/6
'''
__author__ = 'jwj'

from bs4 import BeautifulSoup
import requests


# 一篇小说 类 Model
class ANovel(object):
    def __init__(self, title=None, author=None, cover=None, desc=None, novel_url=None, chapters_url=None):
        self.NovelTitle = title    # 小说名
        self.Author = author       # 小说作者
        self.CoverImgUrl = cover   # 封面图片链接
        self.Desc = desc           # 小说内容的简短介绍
        self.NovelUrl = novel_url  # 小说跳转链接
        self.ChaptersUrl = chapters_url  # 小说目录链接
        self.Chapters = []         # 小说所有章节(chapterTitle, chapterUrl)列表

    # 读取传入参数url的网页源码
    def readHtml(self, url):
        html = requests.get(url)   # 请求url
        html.encoding = 'gbk'
        return html.text

    # 获取该小说所有章节的(title, url)组成的列表Chapters
    def getChaptersUrl(self):
        html = self.readHtml(self.ChaptersUrl)
        soup = BeautifulSoup(html, 'html.parser')
        for chapter in soup.select(".chapterNum ul li a"):
            self.Chapters.append((chapter.string, chapter['href']))  # 章节名及链接加入列表
        return self.Chapters

    # 获取该小说某一章节的小说文本内容，并写入文件 chapter: (chapter_title, chapter_url)
    def getOneChapterContent(self, chapter):
        k = 0
        obj = None
        while k < 3:                                  # 容错
            html = self.readHtml(chapter[1])
            soup = BeautifulSoup(html, 'html.parser')
            obj = soup.find(attrs="mainContenr")
            if obj:
                break
            k += 1
        if not obj:
            print('None')
            return
        content = obj.text
        content_drop = content.replace("style5();", "").replace("style6();", "").replace('<br />', '\n').replace(u'\xa0', u' ').replace(u'\ufffd', u' ')
        self.write2txt(chapter[0], content_drop)

    # 写入txt，传入章节名和该章节对应的文本内容
    def write2txt(self, chapter_name, content):
        with open('Novels/' + self.NovelTitle + '.txt', 'a') as file:
            print(self.NovelTitle + ' 正在写入 ' + chapter_name)
            file.writelines(chapter_name + '\n\n' + content + '\n\n')

