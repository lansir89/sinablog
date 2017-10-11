#coding=utf-8
import sys,time
from selenium import webdriver

#webdriver的自定义chrome类，只是加了个url，其他都继承自系统webdriver.Chrome
class myChrome(webdriver.Chrome):
    homeUrl=""                  