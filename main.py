'''
File Name:    main.py
Description:  主函数，调用其他方法
Author:       jwj
Date:         2018/1/7
'''
__author__ = 'jwj'

from AllNovels import *

if __name__ == '__main__':
    url = 'http://www.quanshuwang.com/list/1_%s.html'
    for page in range(1, 2):                         # range范围可修改
        novelsObjList = get_novels_info(url % page)
        novelsObjList = get_chapters_url(novelsObjList)
        # write2csv(novelsObjList)
        all_chapters_url(novelsObjList)

