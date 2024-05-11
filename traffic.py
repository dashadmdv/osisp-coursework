from scapy.all import *
from get_network import get_network_info, format_network
from check_params import network_param
import ipaddress

def capture_traffic(interface, subnet, max_packets=1000):
    # Преобразуем строку подсети в объект ipaddress.IPv4Network
    network = ipaddress.IPv4Network(subnet, strict=False)
    # Словарь для хранения статистики трафика по IP-адресам
    traffic_stats = defaultdict(lambda: {"sent_bytes": 0, "recv_bytes": 0})

    # Функция обработки захваченных пакетов
    def packet_callback(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            if ipaddress.IPv4Address(src_ip) in network or ipaddress.IPv4Address(dst_ip) in network:
                if TCP in packet:
                    # Если есть TCP заголовок, учитываем количество переданных байт
                    sent_bytes = len(packet[TCP].payload)
                    if ipaddress.IPv4Address(src_ip) in network:
                        traffic_stats[src_ip]["sent_bytes"] += sent_bytes
                    if ipaddress.IPv4Address(dst_ip) in network:
                        traffic_stats[dst_ip]["recv_bytes"] += sent_bytes
                elif UDP in packet:
                    # Если есть UDP заголовок, учитываем количество переданных байт
                    sent_bytes = len(packet[UDP].payload)
                    if ipaddress.IPv4Address(src_ip) in network:
                        traffic_stats[src_ip]["sent_bytes"] += sent_bytes
                    if ipaddress.IPv4Address(dst_ip) in network:
                        traffic_stats[dst_ip]["recv_bytes"] += sent_bytes

    # Захватываем пакеты на указанном интерфейсе
    sniff(iface=interface, prn=packet_callback, count=max_packets)

    return traffic_stats

def main():
    params = network_param()
    interface = params["Default Interface"]
    my_ip = params["IPv4 address"]
    subnet = format_network(*get_network_info())
    traffic_stats = capture_traffic(interface, subnet)

    me = "(данное устройство)"
    print("Статистика трафика:")
    for ip, stats in traffic_stats.items():
        print(f"IP: {ip} {me if ip == my_ip else ''}, Отправлено: {stats['sent_bytes']} байт, Принято: {stats['recv_bytes']} байт")

if __name__ == "__main__":
    main()
