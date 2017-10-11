#coding=utf-8
import pickle
import sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException

#webTool��һ�������࣬����ȫ���෽�������ڸ�����վͨ�õ�һЩ�෽����
class webTool(object):

    def __init__(self):
        return

     # �������ƣ� waitToClick
     # ���������� �ȴ�ָ��������ֲ������һ������
     # ���������obj - ���������
     #         time - �ȴ���ʱ�䣬��λΪ�룬���ȴ�10����
     #         findelement - ��Ҫ�ȴ���ָ������
     #         toBlogUrl - Ҫ�����URL
     # ��������� 
     # �� �� ֵ��obj - ���������
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

     # �������ƣ� waitLoad
     # ���������� �ȴ�ָ���������
     # ���������obj - ���������
     #         time - �ȴ���ʱ�� 
     #         findelement - ��Ҫ�ȴ���ָ������
     # ��������� 
     # �� �� ֵ��1 - ��ʾ˳���ҵ�Ԫ��
     #          0 - ��ʾ�޷��ҵ�Ԫ��
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

     # �������ƣ� cookieLogin
     # ���������� ���cookie�������
     # ���������obj - ���������
     #         cookielist - cookie�б� 
     #         flag - ˢ�±�־λ��0��ʾ����Ҫˢ�£�1��ʾ��Ҫˢ��
     #         iterable - ��Ҫ�ų�����Ч����б�
     #         findEle - �ж�cookie�Ƿ��½�ɹ���xpath����
     # ��������� 
     # �� �� ֵ��obj - ���������
    @classmethod
    def cookieLogin(self,obj,cookielist,flag,iterable,findEle):
        obj.delete_all_cookies()   
        for j in xrange(10):                    #��½ʧ�ܣ������µ�½������½10��
            for cookie in cookielist:
                if cookie["domain"] in iterable:	#�ų���Ч��
                    obj.add_cookie(cookie)
            if flag == 1:                      #ˢ��ҳ��
                obj.refresh()
            if j == 4:
                obj.refresh()
            a=self.waitLoad(obj,3,findEle)
            if a==1:     #����ҵ�ָ���Ķ��󣬱�ʾ�Ѿ���½��
                break
            else:
                sleep(1)
                print "cookie faile"

     # �������ƣ� gotoWindow
     # ���������� ��ת����һ��ҳ�棬�������Ƿ�ر�ԭ��ҳ��
     # ���������obj - ���������
     #         flag - ��־λ��1��ʾ�ر�ָ��ҳ�棬0��ʾ���ر�
     #         oldHandles - �������ǰ������������д��ھ��
     #         Handles - ��ǰ�������ҳ�����б�
     #         gotoHandle - ��Ҫ��ת��ҳ��ľ����Ϊ�����ʾ��ת����ҳ��
     # ��������� 
     # �� �� ֵ��
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

     # �������ƣ� savecookies
     # ���������� ����cookie
     # ���������obj - ���������
     #         website - cookie��������վ
     #         username - �˺���
     # ��������� 
     # �� �� ֵ��
    @classmethod                  
    def saveCookies(self,obj,webSite,username):
        cookies=obj.get_cookies()
        filepkl = ('cookies/%s/%s.%s') % (webSite,username, "pkl")
        pickle.dump(cookies , open(filepkl,"wb"))

     # �������ƣ� getcookies
     # ���������� ��ȡ
     # ���������obj - ���������
     #         website - cookie��������վ
     #         username - �˺���
     # ��������� 
     # �� �� ֵ��cookie�б�
    @classmethod   
    def getcookies(self,webSite,username):
        file = ('cookies/%s/%s.%s') % (webSite,username, "pkl")
        pkl_file = open(file, "rb")
        cookies = pickle.load(pkl_file)
        return cookies 

     # �������ƣ� gethash
     # ���������� ��ȡhash
     # ���������obj - ���������
     #         website - cookie��������վ
     #         username - �˺���
     # ��������� 
     # �� �� ֵ��cookie�б�
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

     # �������ƣ� savehash
     # ���������� ����hash
     # ���������hash - hashֵ
     #         website - cookie��������վ
     #         username - �˺���
     # ��������� 
     # �� �� ֵ��cookie�б�
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