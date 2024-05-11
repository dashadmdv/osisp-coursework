from pysnmp.hlapi import *

def snmp_get(ip, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('dasha', mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(f"Ошибка: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Ошибка: {errorStatus}")
        return None
    else:
        for varBind in varBinds:
            return varBind[1].prettyPrint()


def pretty_time(time: str):
    dot = int(time) % 100
    time = int(time) // 100
    hours = time // 60 // 60
    minutes = (time - hours * 3600) // 60
    seconds = time - hours * 3600 - minutes * 60
    formatted_time = f"{hours}ч:{minutes}мин:{seconds}.{dot}сек"
    return formatted_time


def get_sys_info(ip):
    sys_descr_oid = ".1.3.6.1.2.1.1.1.0"  # OID для описания системы - описание устройства
    sys_name_oid = ".1.3.6.1.2.1.1.5.0"  # имя устройства
    sys_timeup_oid = ".1.3.6.1.2.1.25.1.1.0"  # время работы устройства
    daemon_timeup_oid = ".1.3.6.1.2.1.1.3.0"  # время работы snmp демона


    sys_descr = snmp_get(ip, sys_descr_oid)
    sys_name = snmp_get(ip, sys_name_oid)
    sys_timeup = snmp_get(ip, sys_timeup_oid)
    daemon_timeup = snmp_get(ip, daemon_timeup_oid)

    if sys_descr and sys_name and daemon_timeup:
        sys_descr = ("Описание системы", str(sys_descr))
        sys_name = ("Имя устройства", str(sys_name))
        daemon_timeup = ("Время работы агента SNMP", pretty_time(daemon_timeup))
        sys_timeup = ("Время работы устройства (хоста)", pretty_time(sys_timeup))

        return sys_descr, sys_name, daemon_timeup, sys_timeup
    else:
        return [("Не удалось получить",  "информацию о системе")]


def main():
    ip = "127.0.0.1"

    print("Получение информации о системе...")

    res = get_sys_info(ip)

    if len(res) > 1:
        for item in res:
            print(f"{item[0]}: {item[1]}")
    else:
        print("Не удалось получить информацию о системе")


if __name__ == "__main__":
    main()
