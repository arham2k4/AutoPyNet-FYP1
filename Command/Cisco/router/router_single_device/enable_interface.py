from netmiko import ConnectHandler

def enable_interface():
    device = {
        "device_type": "cisco_ios",
        "ip": "10.10.10.15",
        "username": "admin",
        "password": "cisco123",
    }

    commands = [
        "interface GigabitEthernet0/1",
        "no shutdown"
    ]

    try:
        net_connect = ConnectHandler(**device)
        print(f"\nConnected to {device['ip']}\n")

        print("Enabling interface...")
        output = net_connect.send_config_set(commands)
        print(f"Output:\n{output}")

        net_connect.send_command("write memory")
        print("\nConfiguration saved.")
        net_connect.disconnect()

    except Exception as e:
        print(f"\nFailed to connect to {device['ip']}: {e}")

def main():
    enable_interface()

if __name__ == "__main__":
    main()