#!/usr/bin/env python
# -*- coding: utf-8-*-
import ConfigParser
def getconf():
    ret=[]
    config = ConfigParser.SafeConfigParser()
    config.read("conf.cfg")
    ret.append(config.get("router", "ip"))
    ret.append(config.get("router", "port"))
    ret.append(config.get("router", "user"))
    ret.append(config.get("router", "pwd"))
    return ret
    
    return r
    
def getAdminInfo():
    ret=[]
    config = ConfigParser.SafeConfigParser()
    config.read("conf.cfg")
    ret.append(config.get("card", "prefix"))
    ret.append(config.get("card", "ignore"))
    ret.append(config.get("wifi", "essid"))
    ret.append(config.get("admin", "pwd"))
    return ret
    
def getCardPrefix():
    ret=''
    config = ConfigParser.SafeConfigParser()
    config.read("conf.cfg")
    ret=config.get("card", "prefix")
    return ret
def getESSID():
    ret=''
    config = ConfigParser.SafeConfigParser()
    config.read("conf.cfg")
    ret=config.get("wifi", "essid")
    return ret

def _(_Name):
    if _Name =='user':
        return u'帐号'
    elif _Name=='address':
        return u'IP地址'
    elif _Name=='mac-address':
        return u'物理地址'
    elif _Name=='uptime':
        return u'上网时间'
    elif _Name=='idle-timeout':
        return u'空闲时间'
    elif _Name=='.id':
        return 'ID'
    
