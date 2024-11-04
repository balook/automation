import socket
import sys

def check_ports(hostname, ports):
    open_ports = []
    
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set a timeout for the connection attempt
            result = sock.connect_ex((hostname, port))  # Returns 0 if the port is open
            if result == 0:
                open_ports.append(port)

    return open_ports

if __name__ == "__main__":
    # List of ports to check
    ports_to_check = [8080, 9090, 8888]
    
    # Read hostnames from standard input (pipe)
    for hostname in sys.stdin:
        hostname = hostname.strip()  # Remove any extra whitespace or newline
        if hostname:  # Check if the line is not empty
            # Check the ports for the current hostname
            open_ports = check_ports(hostname, ports_to_check)
            # Output results in the format "hostname:port", one per line
            for port in open_ports:
                print(f"{hostname}:{port}")
