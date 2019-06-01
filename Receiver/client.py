import socket
from ast import literal_eval
from tqdm import tqdm

def main():
    host = socket.gethostname()
    port = 5000
    bytes_dwnld = 1024
    prefix = "new_"

    s = socket.socket()
    s.connect((host, port))

    choices = s.recv(bytes_dwnld).decode('utf-8')
    print(choices)
    client_choice = input("Enter the number to download or 0 to quit -> ")
    if int(client_choice) != 0:
        s.send(client_choice.encode('utf-8'))
        filename = s.recv(bytes_dwnld).decode('utf-8')
        print(filename)
        data = s.recv(bytes_dwnld)
        data = data.decode('utf-8')
        print(data)
        if data[:6] == 'EXISTS':
                filesize = int(data[8:])
                message = input(
                    f"File exists: {str(filesize)} Bytes. Download? (Y/N) -> ")
                if message == 'Y':
                    s.send("OK".encode('utf-8'))
                    file = open(prefix + filename, 'wb')
                    data = s.recv(bytes_dwnld)
                    total_received = len(data)
                    file.write(data)
                    pbar = tqdm(total=filesize, initial=total_received)
                    while total_received < filesize:
                        data = s.recv(bytes_dwnld)
                        total_received += len(data)
                        file.write(data)
                        # stat = (total_received / float(filesize)) * 100
                        # print(f"{stat:.2f} % Done")
                        pbar.update(len(data))
                    else:
                        pbar.close()
                        print("Download Complete!")
        else:
            print("File does not exist")
    else :
        print("Bye")

    s.close()

if __name__ == '__main__':
    main()


