# may/05/2014 16:32:33 by RouterOS 6.12
# software id = UELR-USC3
#
/interface bridge
add l2mtu=2290 name=bridge1
/interface wireless
set [ find default-name=wlan1 ] band=2ghz-b/g/n channel-width=\
    20/40mhz-ht-below country=china disabled=no frequency=2462 
    l2mtu=2290 \
    mode=ap-bridge wireless-protocol=802.11
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity=MikroTik
/ip hotspot
add disabled=no idle-timeout=none interface=bridge1 name=server1
/ip hotspot profile
set [ find default=yes ] http-cookie-lifetime=30m login-by=cookie
,http-pap \
    use-radius=yes
/ip hotspot user profile
set [ find default=yes ] idle-timeout=none keepalive-timeout=2h \
    mac-cookie-timeout=3d shared-users=3
/ip pool
add name=dhcp ranges=192.168.220.100-192.168.220.150
/ip dhcp-server
add address-pool=dhcp disabled=no interface=bridge1 lease-time=30m
name=dhcp1
/interface bridge port
add bridge=bridge1 interface=wlan1
/ip address
add address=192.168.220.1/24 interface=wlan1 network=192.168.220.0
add address=192.168.120.13/24 interface=ether1 network=192.168.120.0
/ip dhcp-client
add dhcp-options=hostname,clientid interface=ether1
/ip dhcp-server network
add address=192.168.220.0/24 dns-server=\
    221.3.131.11,8.8.8.8,202.203.132.1,8.8.4.4 gateway=192.168.220.1 
    netmask=\
    24
/ip dns
set servers=221.3.131.11,8.8.8.8
/ip firewall filter
add action=passthrough chain=unused-hs-chain comment=\
    "place hotspot rules here" disabled=yes
/ip firewall nat
add action=passthrough chain=unused-hs-chain comment=\
    "place hotspot rules here" disabled=yes to-addresses=0.0.0.0
add action=masquerade chain=srcnat out-interface=ether1 to-addresses=
0.0.0.0
/ip route
add distance=1 gateway=192.168.120.1
/ip service
set www port=88
/ip upnp
set allow-disable-external-interface=no
/radius
add address=202.203.132.242 secret=radius service=\
    ppp,login,hotspot,wireless,dhcp timeout=6s
/system clock
set time-zone-name=Etc/GMT-8
/system clock manual
set time-zone=+08:00
/system identity
set name=CS-AP-2.4G-1
/system ntp client
set enabled=yes primary-ntp=216.171.120.36 secondary-ntp=64.4.10.33
/system scheduler
add interval=1d name="Reboot Router" on-event="/system \
    \nreboot" policy=\
    ftp,reboot,read,write,policy,test,winbox,password,sniff,sensitive
    ,api \
    start-date=jan/01/1970 start-time=06:00:00
