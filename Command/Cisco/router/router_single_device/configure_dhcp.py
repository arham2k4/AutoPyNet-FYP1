from netmiko import ConnectHandler

def configure_dhcp():
    device = {
        "device_type": "cisco_ios",
        "ip": "10.10.10.15",
        "username": "admin",
        "password": "cisco123",
    }

    commands = [
        "ip dhcp excluded-address 192.168.10.1 192.168.10.10",
        "ip dhcp pool LAN",
        "network 192.168.10.0 255.255.255.0",
        "default-router 192.168.10.1",
        "dns-server 8.8.8.8"
    ]

    try:
        net_connect = ConnectHandler(**device)
        print(f"\nConnected to {device['ip']}\n")

        print("Configuring DHCP...")
        output = net_connect.send_config_set(commands)
        print(f"Output:\n{output}")

        net_connect.send_command("write memory")
        print("\nConfiguration saved.")
        net_connect.disconnect()

    except Exception as e:
        print(f"\nFailed to connect to {device['ip']}: {e}")

def main():
    configure_dhcp()

if __name__ == "__main__":
    main()