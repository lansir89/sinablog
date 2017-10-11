#coding=utf-8
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from file import myFile
from time import sleep
from lib.webTool import webTool
import sys,time
import re
import random
import requests
import os.path

class sinaBlog(object):
    oldHandles=""
    handles=""
    site="sina"

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        return
    
     # 函数名称： getuser
     # 功能描述： 获取用户账号密码
     # 输入参数：
     # 输出参数： 
     # 返 回 值： 
    def getuser(self):
        uname=myFile.getuname()
        for i in xrange(len(uname)):
            user=uname[i][0]
            pwd=uname[i][1]
            yield user,pwd

     # 函数名称： login
     # 功能描述： 账号登陆
     # 输入参数：obj - 浏览器对象  
     # 输出参数： 
     # 返 回 值：  
    def login(self,obj):
        obj.delete_all_cookies()
        r=self.getuser()
        userlen=len(myFile.getuname())
        print userlen
        for i in xrange(userlen):
            user,pwd=r.next()
            usercookiepath=('cookies/sina/%s.pkl')%(user)                    #账号cookie
            webTool.waitLoad(obj,5,"//div[@id='loginName']")
            if os.path.exists(usercookiepath)==1:                       #存在cookie文件则直接cookie登陆
                self.cookieslogin(obj,user)
            else:
                obj.find_element_by_id("loginName").send_keys(user.decode('utf-8'))
                obj.find_element_by_id("loginPass").send_keys(pwd.decode('utf-8'))
                webTool.waitToClick(obj,5,"//input[@id='loginButton']","//input[@id='loginButton']")
                findEle = "//div[@id='blog_user_logined']/div[1]/div[2]/p[1]/a"
                webTool.waitLoad(obj,5,findEle)
                webTool.saveCookies(obj,self.site,user)
                toBlogUrl = "//div[@id='blog_user_logined']/div[1]/div[2]/h3/a"
                self.oldHandles=obj.window_handles
                obj=webTool.waitToClick(obj,5,findEle,toBlogUrl)
                self.handles=obj.window_handles
                webTool.gotoWindow(obj,1,self.oldHandles,self.handles)
                self.blog(obj,user)
                self.accountClose(obj,self.site,user)

     # 函数名称： cookieslogin
     # 功能描述： cookie登陆
     # 输入参数：obj - 浏览器对象  
     #          username - 账号名
     # 输出参数： 
     # 返 回 值： 
    def cookieslogin(self,obj,username):
        cookielist=webTool.getcookies(self.site,username)
        domain=[".sina.com.cn",".blog.sina.com.cn"]     #cookie的域，一般是跟登陆页面的域名有关，不允许跨域
        webTool.cookieLogin(obj,cookielist,0,domain,"//div[@id='blog_user_logined']/div[1]/div[2]/p[1]/a")
        findEle = "//div[@id='blog_user_logined']/div[1]/div[2]/p[1]/a"
        toBlogUrl = "//div[@id='blog_user_logined']/div[1]/div[2]/h3/a"
        self.oldHandles=obj.window_handles
        webTool.waitToClick(obj,10,findEle,toBlogUrl)
        self.handles=obj.window_handles
        webTool.gotoWindow(obj,1,self.oldHandles,self.handles)        #关闭旧页面后，新页面就成了第1个页面
        obj.homeUrl = obj.current_url
        self.blog(obj,username)
        self.accountClose(obj,self.site,username)

     # 函数名称： blog
     # 功能描述： 发博客
     # 输入参数：obj - 浏览器对象  
     # 输出参数： 
     # 返 回 值：        
    def blog(self,obj,username):
        r=myFile.readfile()    
        for i in xrange(myFile.lenarticle()):
            title,con=r.next()           
            self.fsBlog(obj,title,con)
            hashlist=webTool.gethash("sina",username)
            if hashlist !=0:
                if hash(title) in hashlist:
                    continue
                else:
                    webTool.savehash(hash(title),"sina",username)
            else:
                webTool.savehash(hash(title),"sina",username)
            sleep(5)
            obj.get(obj.homeUrl)

     # 函数名称： blog
     # 功能描述： 具体执行发博客
     # 输入参数：obj - 浏览器对象  
     # 输出参数： title - 博文标题
     #          content - 博文内容
     # 返 回 值： 
    def fsBlog(self,obj,title,content):
        self.oldHandles=obj.window_handles
        webTool.waitToClick(obj,20,"//div[@id='sinablogfooter']/p[1]/a[1]","//a[@id='SG_Publish']")
        self.handles=obj.window_handles
        webTool.gotoWindow(obj,0,self.oldHandles,self.handles)
        for i in xrange(10):            #尝试10次
            if webTool.waitLoad(obj,20,"/html/body/div[2]/div/div[2]/p[1]/a[1]") == 0:  #如果能找到最下面的“新浪BLOG意见反馈留言板”，则表示加载完成
                print u"没有找到指定内容"
                obj.refresh()
                if i == 9:
                    sys.exit()
                sleep(1)
        self.qiandao(obj)
        for i in xrange(10):
            if webTool.waitLoad(obj,20,"//input[@id='articleTitle']") == 1:
                obj.find_element_by_xpath("//input[@id='articleTitle']").send_keys(title)   
            else:
                print u"没有找到指定内容"
                obj.refresh()
                if i == 9:          #如果已经过了10次了，则退出
                    sys.exit()
                sleep(1)
                continue            
            obj.switch_to.frame(obj.find_element_by_xpath("//div[@id='SinaEditor_Iframe']/iframe"))     #切换到iframe编辑器中
            obj.find_element_by_tag_name('body').send_keys(content)
            obj.switch_to.default_content()             #退回出iframe，返回主文档
            if webTool.waitLoad(obj,20,"//form[@id='editorForm']/div/div[6]/ul/li[6]/a") == 1:
                target = obj.find_element_by_xpath("//form[@id='editorForm']/div/div[6]/ul/li[6]/a")    #用于移动滚动条到按钮处
            else:
                print u"没有找到指定内容"
                obj.refresh()
                if i == 9:
                    sys.exit()
                continue
            obj.execute_script("arguments[0].scrollIntoView();", target)
            sleep(2)
            if webTool.waitLoad(obj,20,"//form[@id='editorForm']/div/div[6]/ul/li[6]/a") == 1:
                obj.find_element_by_xpath("//form[@id='editorForm']/div/div[6]/ul/li[6]/a").click()   
                break
            else:
                print u"没有找到指定内容"
                obj.refresh()
                if i == 9:
                    sys.exit()
                continue
            sleep(5)
        if webTool.waitLoad(obj,20,"/html/body/table/tbody/tr/td[2]/div/div/p/a") == 1:
            obj.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/div/div/p/a").click()
        else:
            obj.get(obj.homeUrl)

     # 函数名称： qiandao
     # 功能描述： 签到功能
     # 输入参数：obj - 浏览器对象  
     # 输出参数： 
     # 返 回 值： 
    def qiandao(self,obj):
        if obj.find_element_by_xpath("//div[@id='jf_check']/a").text == u"签到领积分":
            obj.find_element_by_xpath("//div[@id='jf_check']/a").click()
        
     # 函数名称： accountClose
     # 功能描述： 关闭账号，实际上需要更新cookie
     # 输入参数：obj - 浏览器对象  
     # 输出参数： 
     # 返 回 值： 
    def accountClose(self,obj,site,username):
        webTool.saveCookies(obj,site,username)
        obj.delete_all_cookies()

