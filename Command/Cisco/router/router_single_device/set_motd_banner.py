from netmiko import ConnectHandler

def set_motd_banner():
    device = {
        "device_type": "cisco_ios",
        "ip": "10.10.10.15",
        "username": "admin",
        "password": "cisco123",
    }

    commands = [
        'banner motd ^Unauthorized access is prohibited!^'
    ]

    try:
        net_connect = ConnectHandler(**device)
        print(f"\nConnected to {device['ip']}\n")

        print("Setting MOTD banner...")
        output = net_connect.send_config_set(commands)
        print(f"Output:\n{output}")

        net_connect.send_command("write memory")
        print("\nConfiguration saved.")
        net_connect.disconnect()

    except Exception as e:
        print(f"\nFailed to connect to {device['ip']}: {e}")

def main():
    set_motd_banner()

if __name__ == "__main__":
    main()