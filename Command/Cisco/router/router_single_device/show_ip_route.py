from netmiko import ConnectHandler

def show_ip_route():
    device = {
        "device_type": "cisco_ios",
        "ip": "10.10.10.15",
        "username": "admin",
        "password": "cisco123",
    }

    try:
        net_connect = ConnectHandler(**device)
        print(f"\nConnected to {device['ip']}\n")

        print("Fetching IP routing table...")
        output = net_connect.send_command("show ip route")
        print(f"Routing Table:\n{output}")

        net_connect.disconnect()

    except Exception as e:
        print(f"\nFailed to connect to {device['ip']}: {e}")

def main():
    show_ip_route()

if __name__ == "__main__":
    main()