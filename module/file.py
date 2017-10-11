#coding=utf-8
import sys
from selenium import webdriver
from os import listdir
from os.path import isfile, join
reload(sys)
sys.setdefaultencoding('utf-8')

class myFile(object):

    def __init__(self):
        return

     # 函数名称： readfile
     # 功能描述： 读取文件内容
     # 输入参数：
     # 输出参数： 
     # 返 回 值：obj - 浏览器对象
    @classmethod
    def readfile(self):
        articlepath="article/"
        articlelist=[]
        for f in listdir(articlepath):
            article=join(articlepath,f)     #将路径和文件名合并成一个相对路径
            if isfile(article):             #判断是不是一个文件
                articlelist.append(article)
        for i in articlelist:
            f=open(i)
            articlecon=f.read()
            articletitle=i.rstrip(".txt").lstrip("article/") #去除路径和.txt，剩下的就是标题
            yield articletitle.decode('gbk'),articlecon.decode('gbk')   #生成器

     # 函数名称： lenarticle
     # 功能描述： 返回文章数量
     # 输入参数：
     # 输出参数： 
     # 返 回 值：obj - 浏览器对象
    @classmethod
    def lenarticle(self):
        articlepath="article/"
        return len(listdir(articlepath))

     # 函数名称： getuname
     # 功能描述： 获取账号列表
     # 输入参数：
     # 输出参数： 
     # 返 回 值：obj - 浏览器对象
    @classmethod
    def getuname(self):                         #获取账号列表
        uname=[]
        with open('user.txt','r')as f:
            for line in f:
                unamelist = []
                if line.strip()!="":
                    filt = line.split('--')
                    if filt[0].strip()!="" and filt[1]!="":
                        unamelist.append(filt[0].strip())
                        unamelist.append(filt[1].strip())
                        uname.append(unamelist)
                    else:
                        print u"账号或密码有空，请重新检查"
                        sys.exit()
        if len(uname) != 0:
            print u"获取登陆账号成功"
        else:
            print u"读入账号出错，请在账号文件里按格式输入账号"
            sys.exit()
        return uname
