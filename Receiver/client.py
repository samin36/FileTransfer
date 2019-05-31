import socket
from ast import literal_eval

def main():
    host = socket.gethostname()
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    choices = s.recv(1024).decode('utf-8')
    print(choices)
    client_choice = input("Enter the number to download or 0 to quit -> ")
    if int(client_choice) != 0:
        s.send(client_choice.encode('utf-8'))
        filename = s.recv(1024).decode('utf-8')
        print(filename)
        config = s.recv(1024).decode('utf-8')
        config = literal_eval(config)
        data = s.recv(config['bytes'])
        data = data.decode('utf-8')
        if data[:6] == 'EXISTS':
                filesize = int(data[8:])
                message = input(
                    f"File exists: {str(filesize)} Bytes. Download? (Y/N) -> ")
                if message == 'Y':
                    s.send("OK".encode('utf-8'))
                    file = open(config['prefix'] + filename, 'wb')
                    data = s.recv(config['bytes'])
                    total_received = len(data)
                    file.write(data)
                    while total_received < filesize:
                        data = s.recv(config['bytes'])
                        total_received += len(data)
                        file.write(data)
                        stat = (total_received / float(filesize)) * 100
                        print(f"{stat:.2f} % Done")
                    else:
                        print("Download Complete!")
        else:
            print("File does not exist")
    else :
        print("Bye")

    s.close()

if __name__ == '__main__':
    main()


