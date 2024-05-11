import socket

def scan_ports(ip, start_port=0, end_port=2 ** 16 - 1):
    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Установка таймаута для соединения

        result = sock.connect_ex((ip, port))
        if result == 0:
            service = get_service(port)
            open_ports.append((port, service))
        sock.close()

    return open_ports

def get_service(port):
    try:
        service = socket.getservbyport(port)
        return service
    except OSError:
        return "Неизвестна"

def main():
    ip = "192.168.89.4"#"127.0.0.1"  # "192.168.89.4"
    start_port = 0
    end_port = 2 ** 16 - 1

    print(f"Сканирование портов с {start_port} по {end_port} на {ip}...")

    open_ports = scan_ports(ip, start_port, end_port)

    if len(open_ports) == 0:
        print("Открытые порты не обнаружены")
    else:
        print("Список открытых портов:", open_ports)

if __name__ == "__main__":
    main()
