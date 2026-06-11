from netmiko import ConnectHandler

def show_ip_interface_brief():
    device = {
        "device_type": "cisco_ios",
        "ip": "10.10.10.15",
        "username": "admin",
        "password": "cisco123",
    }

    try:
        net_connect = ConnectHandler(**device)
        print(f"\nConnected to {device['ip']}\n")

        print("Running 'show ip interface brief'...")
        output = net_connect.send_command("show ip interface brief")
        print(output)

        net_connect.disconnect()

    except Exception as e:
        print(f"\nFailed to connect to {device['ip']}: {e}")

def main():
    show_ip_interface_brief()

if __name__ == "__main__":
    main()