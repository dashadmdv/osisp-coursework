from scapy.all import ARP, Ether, srp
import subprocess
import re


def get_network_info():
    try:
        output = subprocess.check_output(["ip", "addr", "show"]).decode()
        matches = re.findall(r"inet (\d+\.\d+\.\d+\.\d+)/(\d+)", output)
        for ip, mask in matches:
            if ip != "127.0.0.1":  # Пропускаем loopback интерфейсы
                return ip, mask
    except subprocess.CalledProcessError:
        print("Ошибка при выполнении команды ip addr show")
    return None, None


def format_network(ip, mask):
    # Форматируем IP и маску подсети в строку подсети вида "192.168.1.0/24"
    return f"{ip}/{mask}"


def get_network():
    return format_network(*get_network_info())


def scan_network(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices


if __name__ == "__main__":
    ip, mask = get_network_info()
    if ip and mask:
        network = format_network(ip, mask)
        print("Полученная подсеть:", network)
    else:
        print("Не удалось получить информацию о сетевом интерфейсе")
    devices = scan_network(network)
    print("Список обнаруженных устройств:")
    print("IP\t\t\tMAC Address")
    print("-----------------------------------------")
    for device in devices:
        print(f"{device['ip']}\t\t{device['mac']}")
