
import socket
import threading

nickname = input("chose ur NickName: ")

#server connecting
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

#listening server and sending nickname
def receive():
    while True:
        try:
            #get message from server
            message = client.recv(1024).decode('ascii')
            if message == "Sukana":
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            #close connection
            print('whooopsie!')
            client.close()
            break

# Sending Messages To Server
# inf loop so it can wait for input to fill up
def write():
    while True:
        message = '{}:{}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()