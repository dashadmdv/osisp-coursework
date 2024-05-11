import os
from check_params import network_param

def limit_traffic(ip_address, max_rate):
    params = network_param()
    interface = params["Default Interface"]
    # Определение правила для ограничения входящего трафика
    os.system(f"tc qdisc add dev {interface} root handle 1: htb default 11")
    os.system(f"tc class add dev {interface} parent 1: classid 1:1 htb rate {max_rate}kbit")
    os.system(f"tc filter add dev {interface} protocol ip parent 1: prio 1 u32 match ip src {ip_address} flowid 1:1")

def remove_traffic_limit(ip_address):
    params = network_param()
    interface = params["Default Interface"]
    # Удаление правил для ограничения входящего трафика
    os.system(f"tc filter del dev {interface} protocol ip parent 1: prio 1 u32 match ip src {ip_address} flowid 1:1")


def main():
    ip_address = "192.168.89.4"#"192.168.89.232"  # IP-адрес, для которого будем ограничивать трафик
    max_rate = 1000  # Максимальная скорость в килобитах в секунду
    #
    # limit_traffic(ip_address, max_rate)
    # print(f"Трафик для IP-адреса {ip_address} ограничен до {max_rate} kbps")
    #
    # remove_traffic_limit(ip_address)
    # print(f"Ограничение трафика для IP-адреса {ip_address} снято")

if __name__ == "__main__":
    main()
