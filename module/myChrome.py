#coding=utf-8
import sys,time
from selenium import webdriver

#webdriver���Զ���chrome�ֻ࣬�Ǽ��˸�url���������̳���ϵͳwebdriver.Chrome
class myChrome(webdriver.Chrome):
    homeUrl=""                  