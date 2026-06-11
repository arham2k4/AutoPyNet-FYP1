from netmiko import ConnectHandler

def show_ip_route():
    routers = [
        {"device_type": "cisco_ios", "ip": "10.10.10.15", "username": "admin", "password": "cisco123"},
        {"device_type": "cisco_ios", "ip": "10.10.10.20", "username": "admin", "password": "cisco123"},
    ]

    for router in routers:
        try:
            print(f"\nConnecting to {router['ip']}...")
            connection = ConnectHandler(**router)
            output = connection.send_command("show ip route")
            print(f"\n===== IP Route on {router['ip']} =====")
            print(output)
            connection.disconnect()
        except Exception as e:
            print(f"Error connecting to {router['ip']}: {e}")

def main():
    show_ip_route()

if __name__ == "__main__":
    main()