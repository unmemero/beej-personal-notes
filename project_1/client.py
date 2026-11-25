import socket
import sys

def parse_args():
    print(len(sys.argv))
    if len(sys.argv) < 2:
        "Missing server and port"
        return None
    elif len(sys.argv) == 2:
        address = sys.argv[1]
        return (address, 80)
    elif len(sys.argv) == 3:
        address = sys.argv[1]
        port = int(sys.argv[2])
        return (address, port)
    else:
        address = sys.argv[1]
        port = int(sys.argv[2])
        filename = sys.argv[3]
        return (address, port, filename)

def create_header(host, filename):
    header = f"GET {filename} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    return header.encode("ISO-8859-1")

def socket_connection(connect_details):
    filename = "/"
    if len(connect_details) > 2:
        filename = connect_details[2]
        connect_details = (connect_details[0], connect_details[1])
    s = socket.socket()
    print(f"Connecting to: {connect_details}")
    s.connect(connect_details)
    print("connection established")
    header = create_header(connect_details[0], filename)
    print(f"Header {header} \n Sending...")
    s.sendall(header)
    data = s.recv(4096)
    print("Received data")
    s.close()
    data = data.decode("ISO-8859-1")
    print(data)

if __name__ == "__main__":
    args = parse_args()
    socket_connection(args)