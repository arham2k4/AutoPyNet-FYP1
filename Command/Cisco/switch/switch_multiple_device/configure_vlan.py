from netmiko import ConnectHandler

def configure_vlan():
    switches = [
        {"device_type": "cisco_ios", "ip": "10.10.10.17", "username": "admin", "password": "cisco123"},
        {"device_type": "cisco_ios", "ip": "10.10.10.19", "username": "admin", "password": "cisco123"},
    ]

    commands = [
        "vlan 10",
        "name Marketing",
        "vlan 20",
        "name IT"
    ]

    for switch in switches:
        try:
            print(f"\nConnecting to {switch['ip']}...")
            connection = ConnectHandler(**switch)
            print("Connected. Configuring VLANs...")
            output = connection.send_config_set(commands)
            print(f"Output:\n{output}")
            connection.send_command("write memory")
            connection.disconnect()
            print("Configuration saved and connection closed.\n")
        except Exception as e:
            print(f"Error connecting to {switch['ip']}: {e}")

def main():
    configure_vlan()

if __name__ == "__main__":
    main()