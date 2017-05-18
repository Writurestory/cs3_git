#/usr/bin/env python
#-*- coding: utf-8 -*-

import ctypes
from ctypes import *
#import thread,sys,time

dll=ctypes.windll.LoadLibrary('btlock55L.dll')

global roomid
def getCardNum():
    bPort=1
    strID='QTJDJHC'
    strPWD='201108'

    iCardNo=create_string_buffer(10)
    iGuestSN=create_string_buffer(10)
    iGuestIdx=create_string_buffer(3)
    strDoorID=create_string_buffer(6)
    strSuitDoor=create_string_buffer(12)
    strPubDoor=create_string_buffer(8)
    strBeginTime=create_string_buffer(14)
    strEndTime=create_string_buffer(14)

    dll.Read_Guest_Card.argtypes = [ctypes.c_int,ctypes.c_char_p,
            ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,
            ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,
            ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
    dll.Read_Guest_Card.restypes = ctypes.c_int

    result=dll.Read_Guest_Card(bPort, strID, strPWD, iCardNo, 
            iGuestSN, iGuestIdx, strDoorID, strSuitDoor, 
            strPubDoor, strBeginTime, strEndTime)
    if result == 0:
        return strDoorID.value
    else:
        return ''

# def myThread():
    # global roomid
    # while 1:
        # t = getCardNum()
        # if roomid != t:
            # roomid =t
            # print roomid
        # time.sleep(2)
        
# def main():
    # global roomid
    # try:
        # roomid=''
        # thread.daemon=True
        # thread.start_new_thread(myThread,())
    # except Exception,e:
        # pass


# if __name__=='__main__':
    # #chk_card()
    # main()
