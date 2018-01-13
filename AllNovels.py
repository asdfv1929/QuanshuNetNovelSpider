'''
File Name:     AllNovels
Description:   获取小说页面中所有小说的信息，包括小说名、作者、小说封面链接、内容描述、跳转链接等
Author:        jwj
Date:          2018/1/7
'''
__author__ = 'jwj'

import requests
import csv
from bs4 import BeautifulSoup
from OneNovelContents import ANovel


# 返回页面源码
def readHtml(url):
    html = requests.get(url)  # 请求url
    html.encoding = 'gbk'
    return html.text

# 获取小说信息
def get_novels_info(url):
    novels = []
    html = readHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.select(".seeWell li"):
        title = item.find(attrs='clearfix').text                        # 小说名
        author = item.span.find_all('a')[1].text                        # 作者
        coverImg = item.find('img')['src']                              # 小说封面链接
        desc = item.find('em').text.replace('\n', '').replace(' ', '')  # 内容描述
        novelUrl = item.span.find('a')['href']                          # 小说跳转链接
        #print(title, author, coverImg, desc, novelUrl)
        novel = [title, author, coverImg, desc, novelUrl]
        novels.append(novel)
    return novels


# 将小说信息写入csv文件
def write2csv(novels):
    with open("novels.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        for novel in novels:
            writer.writerow(novel)


# 获取小说跳转至章节的链接
def get_chapters_url(novel_list):
    for novel in novel_list:
        k = 0
        obj = None
        while k < 3:
            html = readHtml(novel[-1])
            soup = BeautifulSoup(html, 'html.parser')
            obj = soup.find(attrs="reader")
            if obj:
                break
            k += 1
        if not obj:
            novel.append('')
            continue
        chapters_url = obj['href']
        novel.append(chapters_url)
    return novel_list


def all_chapters_url(novel_list):
    for novel in novel_list:
        a_novel = ANovel(novel[0], novel[1], novel[2], novel[3], novel[4], novel[5])  # 初始化一个novel对象
        a_novel.getChaptersUrl()                                                      # 获取该小说对象的所有章节的链接
        #print(a_novel.Chapters[:10])                                                 # 打印小说章节列表中的前10章
        for chapter in a_novel.Chapters:              # 遍历该小说的所有章节
            a_novel.getOneChapterContent(chapter)     # 获取某一章节的文本内容

