import socket
import threading
import os
from util import config


def possible_files(sock):
    file_names = [f for f in os.listdir('.') if os.path.isfile(f)]
    files_with_num = [f"{num}. {name}" for num, name in enumerate(file_names, 1)]
    files_list = "\n".join(files_with_num)
    to_send = "Here are the list of available files to download:\n"
    to_send += files_list
    sock.send(to_send.encode('utf-8'))
    choice = int(sock.recv(config['bytes']).decode('utf-8'))
    return file_names[choice - 1]



def retrieve_file(name, sock):
    filename = possible_files(sock)
    sock.send(filename.encode('utf-8'))
    if os.path.isfile(filename):
        sock.send(str(config).encode('utf-8'))
        msg = f"EXISTS: {str(os.path.getsize(filename))}"
        sock.send(msg.encode('utf-8'))
        user_resp = sock.recv(config['bytes'])
        user_resp = user_resp.decode('utf-8')
        if user_resp[:2] == 'OK':
            with open(filename, 'rb') as file:
                bytes_to_send = file.read(config['bytes'])
                sock.send(bytes_to_send)
                while bytes_to_send != '':
                    bytes_to_send = file.read(config['bytes'])
                    sock.send(bytes_to_send)
    else:
        err_msg = "ERR"
        sock.send(err_msg.encode('utf-8'))

    sock.close()

def main():
    # host = socket.gethostname()
    host = ''
    port = 5000

    s = socket.socket()
    s.bind((host, port))
    s.listen(5)

    print("Server Started.")
    conn, addr = s.accept()
    print(f"Client connected ip:<{str(addr)}>")
    # t = threading.Thread(target=retrieve_file, args=('retrThread', conn))
    # t.start()

    # t.stop()
    retrieve_file("Retriever", conn)
    s.close()

if __name__ == '__main__':
    main()

