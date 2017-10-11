#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from time import sleep
from module.file import myFile
from module.functions import sinaBlog
from module.myChrome import myChrome
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2,                  #禁用图片
         "profile.default_content_setting_values.notifications": 2}             #禁用通知
chromeOptions.add_experimental_option("prefs", prefs)
weiboobj = myChrome(chrome_options=chromeOptions)
weiboobj.get('http://blog.sina.com.cn/')

sina_blog=sinaBlog()
sina_blog.login(weiboobj)