from netmiko import ConnectHandler

def configure_ssh():
    device = {
        "device_type": "cisco_ios",
        "ip": "10.10.10.15",
        "username": "admin",
        "password": "cisco123",
    }

    commands = [
        "hostname RouterSSH",
        "ip domain-name localdomain",
        "crypto key generate rsa modulus 1024",
        "ip ssh version 2",
        "username admin privilege 15 secret cisco123",
        "line vty 0 4",
        "transport input ssh",
        "login local"
    ]

    try:
        net_connect = ConnectHandler(**device)
        print(f"\nConnected to {device['ip']}\n")

        print("Configuring SSH...")
        output = net_connect.send_config_set(commands)
        print(f"Output:\n{output}")

        net_connect.send_command("write memory")
        print("\nConfiguration saved.")
        net_connect.disconnect()

    except Exception as e:
        print(f"\nFailed to connect to {device['ip']}: {e}")

def main():
    configure_ssh()

if __name__ == "__main__":
    main()