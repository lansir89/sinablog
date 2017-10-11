#coding=utf-8
import pickle
import sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException

#webTool是一个工具类，里面全是类方法，用于各种网站通用的一些类方法。
class webTool(object):

    def __init__(self):
        return

     # 函数名称： waitToClick
     # 功能描述： 等待指定对象出现并点击另一个对象
     # 输入参数：obj - 浏览器对象
     #         time - 等待的时间，单位为秒，最多等待10分钟
     #         findelement - 需要等待的指定对象
     #         toBlogUrl - 要点击的URL
     # 输出参数： 
     # 返 回 值：obj - 浏览器对象
    @classmethod
    def waitToClick(self,obj,time,findelement,toblogurl):
        for i in xrange(time):
            try:
                obj.find_element_by_xpath(findelement).is_displayed()               
            except NoSuchElementException:
                if i==time-1:
                    print "element is not found"
                    sys.exit()
                sleep(1)
            else:
                obj.find_element_by_xpath(toblogurl).click()
                return obj

     # 函数名称： waitLoad
     # 功能描述： 等待指定对象出现
     # 输入参数：obj - 浏览器对象
     #         time - 等待的时间 
     #         findelement - 需要等待的指定对象
     # 输出参数： 
     # 返 回 值：1 - 表示顺利找到元素
     #          0 - 表示无法找到元素
    @classmethod
    def waitLoad(self,obj,time,findelement):
        for i in xrange(time):
            try:
                obj.find_element_by_xpath(findelement).is_displayed()               
            except NoSuchElementException:
                if i==time-1:
                    return 0
                sleep(1)
            else:
                return 1

     # 函数名称： cookieLogin
     # 功能描述： 添加cookie到浏览器
     # 输入参数：obj - 浏览器对象
     #         cookielist - cookie列表 
     #         flag - 刷新标志位，0表示不需要刷新，1表示需要刷新
     #         iterable - 需要排除的无效域的列表
     #         findEle - 判断cookie是否登陆成功的xpath对象
     # 输出参数： 
     # 返 回 值：obj - 浏览器对象
    @classmethod
    def cookieLogin(self,obj,cookielist,flag,iterable,findEle):
        obj.delete_all_cookies()   
        for j in xrange(10):                    #登陆失败，则重新登陆，最多登陆10次
            for cookie in cookielist:
                if cookie["domain"] in iterable:	#排除无效域
                    obj.add_cookie(cookie)
            if flag == 1:                      #刷新页面
                obj.refresh()
            if j == 4:
                obj.refresh()
            a=self.waitLoad(obj,3,findEle)
            if a==1:     #如果找到指定的对象，表示已经登陆了
                break
            else:
                sleep(1)
                print "cookie faile"

     # 函数名称： gotoWindow
     # 功能描述： 跳转到另一个页面，并设置是否关闭原有页面
     # 输入参数：obj - 浏览器对象
     #         flag - 标志位，1表示关闭指定页面，0表示不关闭
     #         oldHandles - 点击链接前的浏览器的所有窗口句柄
     #         Handles - 当前浏览器的页面句柄列表
     #         gotoHandle - 需要跳转的页面的句柄，为空则表示跳转到新页面
     # 输出参数： 
     # 返 回 值：
    @classmethod
    def gotoWindow(self,obj,flag,oldHandles,newHandles,gotoHandle=""):
        
        if flag == 1:
            if gotoHandle != "":
                obj.close()
                obj.switch_to_window(gotoHandle) 
            else:
                for handleTmp in newHandles:
                    if handleTmp not in oldHandles:
                        obj.close()
                        obj.switch_to_window(handleTmp)    
        else:
            if gotoHandle != "":
                obj.switch_to_window(gotoHandle) 
            else:
                for handleTmp in newHandles:
                    if handleTmp not in oldHandles:
                        obj.switch_to_window(handleTmp)  

     # 函数名称： savecookies
     # 功能描述： 保存cookie
     # 输入参数：obj - 浏览器对象
     #         website - cookie所属的网站
     #         username - 账号名
     # 输出参数： 
     # 返 回 值：
    @classmethod                  
    def saveCookies(self,obj,webSite,username):
        cookies=obj.get_cookies()
        filepkl = ('cookies/%s/%s.%s') % (webSite,username, "pkl")
        pickle.dump(cookies , open(filepkl,"wb"))

     # 函数名称： getcookies
     # 功能描述： 获取
     # 输入参数：obj - 浏览器对象
     #         website - cookie所属的网站
     #         username - 账号名
     # 输出参数： 
     # 返 回 值：cookie列表
    @classmethod   
    def getcookies(self,webSite,username):
        file = ('cookies/%s/%s.%s') % (webSite,username, "pkl")
        pkl_file = open(file, "rb")
        cookies = pickle.load(pkl_file)
        return cookies 

     # 函数名称： gethash
     # 功能描述： 获取hash
     # 输入参数：obj - 浏览器对象
     #         website - cookie所属的网站
     #         username - 账号名
     # 输出参数： 
     # 返 回 值：cookie列表
    @classmethod   
    def gethash(self,webSite,username):
        file = ('cookies/%s/hash.%s') % (webSite,"pkl")
        pkl_file = open(file, "rb")
        try:
            hashlist = pickle.load(pkl_file)
        except EOFError:
            return 0
        for i in hashlist:
            if i["name"] == username:
                return i["values"] 
        else:
            return 0

     # 函数名称： savehash
     # 功能描述： 保存hash
     # 输入参数：hash - hash值
     #         website - cookie所属的网站
     #         username - 账号名
     # 输出参数： 
     # 返 回 值：cookie列表
    @classmethod   
    def savehash(self,hash,webSite,username):
        file = ('cookies/%s/hash.%s') % (webSite,"pkl")
        pkl_file = open(file, "rb")
        try:
            hashlist = pickle.load(pkl_file)
        except EOFError:
            hashlist=[]
            hashdict={}
            hashdictvalue=[]
            hashdict["name"]=username
            hashdictvalue.append(hash)
            hashdict["values"]=hashdictvalue
            hashlist.append(hashdict)
        else:
            for i in hashlist:
                if i["name"] == username:
                    i["values"].append(hash) 
            else:
                hashdict={}
                hashdictvalue=[]
                hashdict["name"]=username
                hashdictvalue.append(hash)
                hashdict["values"]=hashdictvalue
                hashlist.append(hashdict)
        pkl_file = open(file, "wb")
        pickle.dump(hashlist,pkl_file)

if __name__=='__main__':
    a=webTool.gethash("sina","812819745")
    print a
    b="678"
    if a==0:
        webTool.savehash(b,"sina","812819745")
    else:
        if b not in a:
            webTool.savehash(b,"sina","812819745")