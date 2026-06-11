from netmiko import ConnectHandler

def enable_interface():
    routers = [
        {"device_type": "cisco_ios", "ip": "10.10.10.15", "username": "admin", "password": "cisco123"},
        {"device_type": "cisco_ios", "ip": "10.10.10.20", "username": "admin", "password": "cisco123"},
    ]

    commands = [
        "interface GigabitEthernet0/1",
        "no shutdown"
    ]

    for router in routers:
        try:
            print(f"\nConnecting to {router['ip']}...")
            connection = ConnectHandler(**router)
            print("Enabling interface...")
            output = connection.send_config_set(commands)
            print(f"Output:\n{output}")
            connection.send_command("write memory")
            connection.disconnect()
            print("Configuration saved and connection closed.\n")
        except Exception as e:
            print(f"Error connecting to {router['ip']}: {e}")

def main():
    enable_interface()

if __name__ == "__main__":
    main()