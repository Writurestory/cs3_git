# -*- coding: utf-8 -*-
#
# by oldj
# http://oldj.net/
#
import sys 
import random
import ros
import myconf
import rasprint

keystr = ''
cardid = ''
PWDSTR='0123456789'

cardPrefix,ignore,ESSID,adminPwd=myconf.getAdminInfo()

def getNewPwd():
    lst=list(PWDSTR)
    slice = random.sample(lst, 6)
    return ''.join(slice)

def checkUser(_user):
    _user="".join(_user.split()); 
    ret=''
    #try:
    #    t=int(_user)
    #    return _user
    #except:
    #    return ''
    #print "The length of card",len(_user)
    
    try:
        if len(_user)==10:
            #检查卡号的前几位
            l=len(cardPrefix)
            #print "compare to ",_user[:6],cardPrefix
            if _user[:6]!=cardPrefix: return ''
            #print "success"
            t=int(_user[-4:])
            #ret= "%04x" %t
            return str(t)
        elif len(_user)==4:
            int(_user,16)
            return _user
        else:
            return ''
    except:
        return ''

def proc_user(cardInput=''):
    #print "enter-----------"
    #2.修改数据库中的用户状态
    _user=str(cardInput)
    #print "proc useing",_user,cardPrefix,ignore,ESSID
    if _user == '': return
    u=checkUser(_user)
    
    if u == '':
        return

    current_user=u

    newPwd=getNewPwd()
    #判断文本框中的用户是否已经存在

    #showUserInfo
    user_list=ros.getUserList(ignore)
    #print "success getUserList"
    #return
    user_blocked_List=[]


    uPosition = -1
    for i in range(0,len(user_list)):
        if user_list[i][1]==current_user: 
            uPosition = i
            break
    #print "uPos %d" %uPosition

    if uPosition != -1:
        #存在,则删除用户,禁止使用
        userid=user_list[uPosition][0]
        user=user_list[uPosition][1]
        ros.delUser(userid,user)
        #存在则修改密码
        #ros.changePwd(userid,newPwd)
        #winsound.Beep(4000,300)
    else:
        #若不存在,添加用户并启用
        ros.addNewUser(current_user,newPwd)
        #winsound.Beep(3000,300)
        #myPrint.send_to_printer(ESSID,current_user,newPwd)
        #print "This is printer",ESSID,current_user,newPwd
	rasprint.raspout(ESSID,current_user,newPwd)

def getpass():
    import termios, sys # man termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ISIG & ~termios.ECHO   # lflags
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        cardid = raw_input()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return cardid
 
def main():
	while 1:
		keystring = getpass()
		proc_user(keystring)
		if keystring == "matriux":
			break
		print keystring
 
if __name__ == "__main__":
    main()
