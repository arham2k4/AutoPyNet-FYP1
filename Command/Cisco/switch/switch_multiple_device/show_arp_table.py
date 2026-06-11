from netmiko import ConnectHandler

def show_arp_table():
    switches = [
        {"device_type": "cisco_ios", "ip": "10.10.10.17", "username": "admin", "password": "cisco123"},
        {"device_type": "cisco_ios", "ip": "10.10.10.19", "username": "admin", "password": "cisco123"},
    ]

    for switch in switches:
        try:
            print(f"\nConnecting to {switch['ip']}...")
            connection = ConnectHandler(**switch)
            output = connection.send_command("show ip arp")
            print(f"\n===== ARP Table on {switch['ip']} =====")
            print(output)
            connection.disconnect()
        except Exception as e:
            print(f"Error connecting to {switch['ip']}: {e}")

def main():
    show_arp_table()

if __name__ == "__main__":
    main()