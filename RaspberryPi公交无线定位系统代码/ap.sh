#!/bin/sh
killall named
ifconfig wlan0 10.1.1.1 netmask 255.255.255.0
iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o ppp0 -j MASQUERADE
iptables -A FORWARD -s 10.1.1.0/24 -o ppp0 -j ACCEPT
iptables -A FORWARD -d 10.1.1.0/24 -m conntrack --ctstate ESTABLISHED,RELATED -i ppp0 -j ACCEPT
echo "1">/proc/sys/net/ipv4/ip_forward
hostapd -B /etc/hostapd/hostapd.conf
/etc/init.d/dnsmasq restart
