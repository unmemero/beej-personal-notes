import sys
import socket
import os
from datetime import datetime
RN = "\r\n"

def parse_args():
    port = None
    if len(sys.argv) < 2:
        port = 8080
        return port
    
    try:
        port = int(sys.argv[1])

    except ValueError:
        print(f"<br />{RN}{sys.argv[1]} is not a valid port number{RN}")
        return None

    if port < 1024 or port > 65535:
        print(f"<br />{RN}{port} is not a valid port number{RN}")
        return None

    return port

def format_file(file_path):
    content = ""

    with open(file_path) as f:
        lines = f.read().splitlines()

    for line in lines:
        content += f"{line}{RN}"

    return content

def find_file(path):
    full_path = f"{os.getcwd()}/{path.lstrip('/')}"
    
    if not os.path.exists(f"{full_path}"):
        return ("404", f"<br />{RN}File/Path does not exist. Please verify the filepath{RN}<br />{RN}", full_path)

    # Check if path is a directory
    if os.path.isdir(full_path):
        # Check if html or txt is available
        ext = "html" if os.path.exists(f"{full_path}/index.html") else "txt"
        full_path = f"{full_path}/index.{ext}"

        if not os.path.exists(full_path):
            return ("404",f"<br />{RN}File/Path does not exist. Please verify the filepath{RN}<br />{RN}", full_path)

    return ("200",format_file(full_path), full_path)

def build_response(code, content, full_path):
    response_status = 'OK' if code == '200' else 'File Not Found'
    current_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    last_modified = current_date if code =='404' else os.path.getmtime(full_path)
    resp = f"HTTP/1.1 {code} {response_status}{RN}Date: {current_date}{RN}Content-Type: text/html; charset=UTF-8{RN}Etag: {hash(full_path)}{RN}Last-Modified: {last_modified}{RN}Vary: Accept-Encoding{RN}Content-Length: {len(content.encode('ISO-8859-1'))}{RN}Connection: close{RN}{RN}{content}"

    return resp.encode("ISO-8859-1")

def socket_connections(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", port))
    s.listen()
    while True:
        new_socket, new_conn = s.accept()
        print(datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"), " New connection from: ", new_conn)
        data = new_socket.recv(1024).decode("ISO-8859-1")
        while f"{RN}{RN}" not in data:
            received = new_socket.recv(1024).decode("ISO-8859-1")
            if len(received) == 0:
                break
            data += received
        
        print(datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"), "Request:", (data.split(RN)))
        if len(data) == 0:
            new_socket.close()
            continue

        data = data.split(RN)
        path = data[0].split(' ')[1]

        code, content, full_path = find_file(path)
        response = build_response(code, content, full_path)
        print(datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"), " Code: ", code, ". Path requested:: ", full_path)
        new_socket.sendall(response)
        print(datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"), "Sent data to requestor. Connection closing\n")
        new_socket.close()

    s.close()
        
if __name__ == "__main__":
    port = parse_args()
    if port == None:
        port = 8080
    socket_connections(port)