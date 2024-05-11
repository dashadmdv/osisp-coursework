import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from check_params import network_param
from get_network import get_network, scan_network
from public_ip import public_ip, geo_ip, get_city
from scan_ports import scan_ports
from snmp import get_sys_info
from traffic import capture_traffic
from speed_test import test_network_speed
from traffic_limit import limit_traffic, remove_traffic_limit

def create_empty_window(title):
    new_window = tk.Toplevel()
    new_window.title(title)
    new_window.geometry("600x400")

    return new_window

# информация о себе

def show_network_info():
    new_window = create_empty_window("Информация о текущей сети")

    # Создаем кнопку для отображения локальной информации
    btn_local = tk.Button(new_window, text="Мои локальные данные", command=show_local_network_info)
    btn_local.pack(pady=(150,5))

    # Создаем кнопку для отображения публичной информации
    btn_public = tk.Button(new_window, text="Мои публичные данные", command=show_public_network_info)
    btn_public.pack(pady=5)


def show_local_network_info():
    new_window = create_empty_window("Мои локальные данные")

    # Получаем информацию о локальных сетевых интерфейсах
    tree = ttk.Treeview(new_window, columns=("Property", "Value"), show="headings")
    tree.heading("Property", text="Свойство")
    tree.heading("Value", text="Значение")
    tree.pack(padx=10, pady=10)

    local_params = network_param()
    subnet = get_network()
    # Заполняем таблицу данными
    data = [
        ("Интерфейс", local_params["Default Interface"]),
        ("IPv4 адрес", local_params["IPv4 address"]),
        ("IPv6 адрес", local_params["IPv6 address"]),
        ("Адрес подсети", subnet),
        ("Адрес роутера", local_params["Router ip-address"]),
        ("MAC адрес", local_params["MAC-address"])
    ]

    for prop, val in data:
        tree.insert("", tk.END, values=(prop, val))

def show_public_network_info():
    # Создаем новое окно для отображения публичной информации о текущей сети
    new_window = create_empty_window("Мои публичные данные")

    tree = ttk.Treeview(new_window, columns=("Property", "Value"), show="headings")
    tree.heading("Property", text="Свойство")
    tree.heading("Value", text="Значение")
    tree.pack(padx=10, pady=10)

    ip = public_ip()
    coordinates = geo_ip(ip)
    place = get_city(coordinates)
    place_str = str(place)
    place_str = place_str.split(', ')
    if len(place_str) > 1:
        place_pt1 = str(place_str[0])
        place_pt2 = str(place_str[1])
        place_pt3 = ', '.join(place_str[2:4])
        place_pt4 = ', '.join(place_str[4:])
        # Заполняем таблицу данными
        data = [
            ("Мой публичный IP адрес", ip),
            ("Координаты IP адреса", coordinates),
            ("Местоположение IP адреса", place_pt1),
            (" ", place_pt2),
            (" ", place_pt3),
            (" ", place_pt4),
        ]
    else:
        data = [
            ("Мой публичный IP адрес", ip),
            ("Координаты IP адреса", coordinates),
            ("Местоположение IP адреса", ''.join(place))
        ]

    for prop, val in data:
        tree.insert("", tk.END, values=(prop, val))


def show_network_devices():
    new_window = create_empty_window("Устройства текущей сети")

    subnet = get_network()
    label = tk.Label(new_window, text=f"Текущая подсеть: {subnet}")
    label.pack(pady=5)

    label = tk.Label(new_window, text=f"Устройства в подсети")
    label.pack(pady=(5, 0))
    tree = ttk.Treeview(new_window, columns=("Property", "Value"), show="headings")
    tree.heading("Property", text="IP-адрес")
    tree.heading("Value", text="MAC-адрес")
    tree.pack(padx=10, pady=10)

    local_params = network_param()
    me = [{'ip': str(local_params["IPv4 address"]) + " (я)" , 'mac': local_params["MAC-address"]}]
    devices = scan_network(subnet)

    devices = me + devices

    data = [ (device['ip'], device['mac']) for device in devices ]

    for prop, val in data:
        tree.insert("", tk.END, values=(prop, val))


def show_ports():
    new_window = create_empty_window("Сканирование портов")

    local_params = network_param()
    default_ip = str(local_params["IPv4 address"])
    entry_ip = tk.Entry(new_window)
    entry_ip.insert(0, default_ip)
    entry_ip.pack(pady=10)

    tree = ttk.Treeview(new_window, columns=("Property", "Value"), show="headings")
    tree.heading("Property", text="Номер порта")
    tree.heading("Value", text="Служба")
    tree.pack(padx=10, pady=10)

    ports = None
    def scan_ports_button():
        nonlocal ports
        ports = scan_ports(entry_ip.get())

        # Удаляем все элементы из таблицы перед заполнением новыми данными
        for item in tree.get_children():
            tree.delete(item)

        data = ports

        for prop, val in data:
            tree.insert("", tk.END, values=(prop, val))

    # Создаем кнопку для сканирования портов
    btn_scan = tk.Button(new_window, text="Сканировать порты", command=scan_ports_button)
    btn_scan.pack()


def show_snmp_scan():
    new_window = create_empty_window("SNMP сканирование")

    default_ip = "127.0.0.1"
    entry_ip = tk.Entry(new_window)
    entry_ip.insert(0, default_ip)
    entry_ip.pack(pady=10)

    tree = ttk.Treeview(new_window, columns=("Property", "Value"), show="headings")
    tree.heading("Property", text="Характеристика")
    tree.heading("Value", text="Значение")
    tree.pack(padx=10, pady=10)

    descr = None

    def snmp_button():
        nonlocal descr
        descr = get_sys_info(entry_ip.get())

        # Удаляем все элементы из таблицы перед заполнением новыми данными
        for item in tree.get_children():
            tree.delete(item)

        data = descr

        for prop, val in data:
            tree.insert("", tk.END, values=(prop, val))

    btn_scan = tk.Button(new_window, text="SNMP запрос", command=snmp_button)
    btn_scan.pack()


def limit_speed():
    new_window = create_empty_window("Ограничение трафика")

    label = tk.Label(new_window, text=f"Ограничение на отправку пакетов (Кбит/с)")
    label.pack(pady=5)
    entry_rate = tk.Entry(new_window)
    entry_rate.pack(pady=10)

    subnet = get_network()
    devices = scan_network(subnet)
    net_ips = [ str(device['ip']) for device in devices ]

    local_params = network_param()
    me = str(local_params["IPv4 address"])
    net_ips.append(me)

    label = tk.Label(new_window, text=f"Ограничиваемый IP")
    label.pack(pady=5)
    combobox = ttk.Combobox(new_window, values=net_ips)
    combobox.pack(padx=10, pady=10)

    def limit():
        limit_traffic(combobox.get(), entry_rate.get())
        msg = "Трафик успешно ограничен"
        mb.showinfo( "ОК", msg)

    btn_scan = tk.Button(new_window, text="Ограничить", command=limit)
    btn_scan.pack()

    def unlimit():
        remove_traffic_limit(combobox.get())
        msg = "Ограничение трафика снято"
        mb.showinfo("ОК", msg)

    btn_unlim = tk.Button(new_window, text="Отменить ограничение", command=unlimit)
    btn_unlim.pack()


def show_traffic_analysis():
    new_window = create_empty_window("Анализ трафика")

    tree = ttk.Treeview(new_window, columns=("Property", "Value1", "Value2"), show="headings")
    tree.heading("Property", text="IP адрес")
    tree.heading("Value1", text="Отправлено (байт)")
    tree.heading("Value2", text="Принято (байт)")
    tree.pack(padx=10, pady=10)

    def traffic_button():
        params = network_param()
        interface = params["Default Interface"]
        my_ip = params["IPv4 address"]
        subnet = get_network()
        traffic_stats = capture_traffic(interface, subnet)

        me = "(я)"
        data = []
        for ip, stats in traffic_stats.items():
            data.append((f"{ip} {me if ip == my_ip else ''}",
                         f"{stats['sent_bytes']}",
                         f"{stats['recv_bytes']}"))

        # Удаляем все элементы из таблицы перед заполнением новыми данными
        for item in tree.get_children():
            tree.delete(item)

        for prop, val1, val2 in data:
            tree.insert("", tk.END, values=(prop, val1, val2))

    btn_scan = tk.Button(new_window, text="Статистика", command=traffic_button)
    btn_scan.pack()

    def test_speed():
        new_window_ = create_empty_window("Скорость сети")
        download, upload = test_network_speed()
        label = tk.Label(new_window_, text=f"Скорость принятия пакетов: {download} Мбит/с")
        label.pack(pady=(150, 10))

        label = tk.Label(new_window_, text=f"Скорость отправки пакетов: {upload} Мбит/с")
        label.pack(pady=5)

    btn_scan = tk.Button(new_window, text="Тест скорости", command=test_speed)
    btn_scan.pack()

    btn_scan = tk.Button(new_window, text="Ограничить трафик", command=limit_speed)
    btn_scan.pack()


def main():
    # Создаем основное окно
    root = tk.Tk()
    root.title("Главное меню")
    root.geometry("600x400")

    # Создаем кнопки для каждого пункта меню
    btn_network_info = tk.Button(root, text="Информация о текущей сети", command=show_network_info)
    btn_network_info.pack(pady=(100, 5))

    btn_network_devices = tk.Button(root, text="Устройства текущей сети", command=show_network_devices)
    btn_network_devices.pack(pady=5)

    btn_ports = tk.Button(root, text="Сканирование портов", command=show_ports)
    btn_ports.pack(pady=5)

    btn_snmp_scan = tk.Button(root, text="SNMP сканирование", command=show_snmp_scan)
    btn_snmp_scan.pack(pady=5)

    btn_traffic_analysis = tk.Button(root, text="Анализ трафика", command=show_traffic_analysis)
    btn_traffic_analysis.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
