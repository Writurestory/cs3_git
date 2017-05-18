#!/usr/bin/env python
# -*- coding: utf-8-*-

import sys, time, md5, binascii, socket, select
import threading
import myconf


class ApiRos:
    "Routeros api"
    def __init__(self):        
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r=myconf.getconf()
        self.sk.connect((r[0],int(r[1])))
        self.login(r[2], r[3]);
        self.currenttag = 0

    def login(self, username, pwd):
        for repl, attrs in self.talk(["/login"]):
            chal = binascii.unhexlify(attrs['=ret'])
        md = md5.new()
        md.update('\x00')
        md.update(pwd)
        md.update(chal)
        self.talk(["/login", "=name=" + username,
                   "=response=00" + binascii.hexlify(md.digest())])
    def talk(self, words):
        if self.writeSentence(words) == 0: return
        r = []
        while 1:
            i = self.readSentence();
            if len(i) == 0: continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find('=', 1)
                if (j == -1):
                    attrs[w] = ''
                else:
                    attrs[w[:j]] = w[j+1:]
            r.append((reply, attrs))
            if reply == '!done': return r

    def writeSentence(self, words):
        ret = 0
        for w in words:
            self.writeWord(w)
            ret += 1
        self.writeWord('')
        return ret

    def readSentence(self):
        r = []
        while 1:
            w = self.readWord()
            if w == '': return r
            r.append(w)
            
    def writeWord(self, w):
        #print "<<< " + w
        self.writeLen(len(w))
        self.writeStr(w)

    def readWord(self):
        ret = self.readStr(self.readLen())
        #print ">>> " + ret
        return ret

    def writeLen(self, l):
        if l < 0x80:
            self.writeStr(chr(l))
        elif l < 0x4000:
            l |= 0x8000
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x200000:
            l |= 0xC00000
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x10000000:        
            l |= 0xE0000000         
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        else:                       
            self.writeStr(chr(0xF0))
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))

    def readLen(self):              
        c = ord(self.readStr(1))    
        if (c & 0x80) == 0x00:      
            pass                    
        elif (c & 0xC0) == 0x80:    
            c &= ~0xC0              
            c <<= 8                 
            c += ord(self.readStr(1))    
        elif (c & 0xE0) == 0xC0:    
            c &= ~0xE0              
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
        elif (c & 0xF0) == 0xE0:    
            c &= ~0xF0              
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
        elif (c & 0xF8) == 0xF0:    
            c = ord(self.readStr(1))     
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
            c <<= 8                 
            c += ord(self.readStr(1))    
        return c                    

    def writeStr(self, str):        
        n = 0;                      
        while n < len(str):         
            r = self.sk.send(str[n:])
            if r == 0: raise RuntimeError, "connection closed by remote end"
            n += r                  

    def readStr(self, length):      
        ret = ''                    
        while len(ret) < length:    
            s = self.sk.recv(length - len(ret))
            if s == '': raise RuntimeError, "connection closed by remote end"
            ret += s
        return ret

def getUserList(ignoreAccount=''):
    apiros = ApiRos();             
    #apiros.login('admin', '');
    inputsentence=['/ip/hotspot/user/print']
    inputsentence.append('=.proplist=.id,name,password,disabled')
    apiros.writeSentence(inputsentence)
    il=len(ignoreAccount)
    ret=[]
    while 1:
        x = apiros.readSentence()
        if x[0] == '!done': break
        del x[0]
        #print ignoreAccount
        #print il
        ipre = x[1].split('=')[2][:il]
        if ipre == ignoreAccount:
           # print "ignore"
            continue
        for i in range(len(x)):
            s=x[i].split('=')
            x[i]=s[2]         
        #print x[6]
        if x[3] == 'false':
            x[3]=u'启用'
        else:
            x[3]=u'禁用'
            x[2]='----'

        ret.append(x)
        
    mySort2(ret,1)
    return ret

def mySort2( A, indexLie=0):
    NLie = len(A[0])
    if indexLie<0:
       indexLie=0
    elif indexLie>=NLie :
        indexLie = 0
    if indexLie!= 0:
        for H in range( len(A)):
            (A[H][0],A[H][indexLie]) = (A[H][indexLie],A[H][0])
    A.sort()
    if indexLie!= 0:
        for H in range( len(A)):
            (A[H][0],A[H][indexLie]) = (A[H][indexLie],A[H][0])
            
def addNewUser(userid,newPwd):
    apiros = ApiRos()
    inputsentence=['/ip/hotspot/user/add']
    inputsentence.append('=name='+userid)
    inputsentence.append('=password='+newPwd)
    inputsentence.append('=server=hotspot1')
    inputsentence.append('=profile=default')
    inputsentence.append('=disabled=false')

    apiros.writeSentence(inputsentence)
    apiros.readSentence()

def changePwd(userid,newPwd):
    apiros = ApiRos()
    inputsentence=['/ip/hotspot/user/set']
    inputsentence.append('=.id='+userid)
    inputsentence.append('=password='+newPwd)
    apiros.writeSentence(inputsentence)
    apiros.readSentence()
    
def delUser(userid,user):
    apiros = ApiRos() 
    inputsentence=['/ip/hotspot/user/remove']
    inputsentence.append('=.id='+userid)
    apiros.writeSentence(inputsentence)
    apiros.readSentence()
    #tickFromLine
    inputsentence=['/ip/hotspot/active/print']
    inputsentence.append('=.proplist=.id,user')
    inputsentence.append('?user='+user)
    apiros.writeSentence(inputsentence)
    #print "user:"+ user
    ret=[]
    while 1:
        x = apiros.readSentence()
        #ret=apiros.readSentence()
        if x[0] == '!done': break
        ret.append(x)
    
    for x in ret:
        t=x.index("=user="+user) 
        #if t>0: 
        acid=x[t-1]
        acid=acid.split('=')[2]
        #print "acid remove:"+acid
        inputsentence=['/ip/hotspot/active/remove']
        inputsentence.append("=.id="+acid)
        apiros.writeSentence(inputsentence)
        while 1:
            xx = apiros.readSentence()
            if xx[0] == '!done': break



def enabledUser(userid,newPwd):
    apiros = ApiRos();             
    inputsentence=['/ip/hotspot/user/set']
    inputsentence.append('=.id='+userid)
    inputsentence.append('=password='+newPwd)
    inputsentence.append('=disabled=false')
    apiros.writeSentence(inputsentence)
    apiros.readSentence()

def activeUserInfo(user,ulist):
    ret=[]
    for t in range(0,len(ulist)):
        if ulist[t][2]=='=user='+user:
            ret.append(ulist[t])
    
    return ret
       
    #while 1:
    #    x = apiros.readSentence()
    #    if x[0] == '!done': break
    #    ret.append(x)
    #return ret

        #apiros.readSentence()
def listActiveUser():
    apiros = ApiRos();             
    inputsentence=['/ip/hotspot/active/print']
    inputsentence.append('=.proplist=.id,user,address,mac-address,uptime
            ,idle-timeout')
    apiros.writeSentence(inputsentence)
    #print "Treading start"
    ret=[]
    while 1:
        x = apiros.readSentence()
        if x[0] == '!done': break
        ret.append(x)
        
    #self.acu_list = ret
    #print self.acu_list
    return ret


def disabledUser(userid,user):
    apiros = ApiRos();             
    inputsentence=['/ip/hotspot/user/set']
    inputsentence.append('=.id='+userid)
    inputsentence.append('=disabled=true')
    apiros.writeSentence(inputsentence)
    apiros.readSentence()
    #tickFromLine
    inputsentence=['/ip/hotspot/active/print']
    inputsentence.append('=.proplist=.id,user')
    apiros.writeSentence(inputsentence)
    #print "user:"+ user
    ret=[]
    while 1:
        x = apiros.readSentence()
        if x[0] == '!done': break
        ret.append(x)

    for x in ret:
        t=x.index("=user="+user) 
        if t>0: 
            acid=x[t-1]
            acid=acid.split('=')[2]
            #print "acid remove:"+acid

            inputsentence=['/ip/hotspot/active/remove']
            inputsentence.append("=.id="+acid)
            apiros.writeSentence(inputsentence)
            while 1:
                xx = apiros.readSentence()
                if xx[0] == '!done': break
            break

    

def main():
    apiros = ApiRos();
    #apiros.login(sys.argv[2], sys.argv[3]);
    
    inputsentence = []

    while 1:
       #r = select.select([s, sys.stdin], [], [], None)
        #if s in r[0]:
            # something to read in socket, read sentence
     

        #if sys.stdin in r[0]:
            # read line from input and strip off newline
        l = sys.stdin.readline()
        l = l[:-1]

            # if empty line, send sentence and start with new
            # otherwise append to input sentence
        if l == '':
            apiros.writeSentence(inputsentence)
            inputsentence = []
        else:
            inputsentence.append(l)
                
        x = apiros.readSentence()
        print x

if __name__ == '__main__':
    main()
