
import socket
import threading

nickname = input("chose ur NickName: ")
if nickname == 'admin':
    password = input("enter password for adminstrator:  ")

#server connecting
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False

#listening server and sending nickname
def receive():
    while True:
        global stop_thread
        if stop_thread: break
        
        try:
            #get message from server
            message = client.recv(1024).decode('ascii')
            if message == "NICKNAME":
                client.send(nickname.encode('ascii'))
                
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASSWORD':
                    client.send(password.encode('ascii'))
                    
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('connection was refused wrong password! ')
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refuesed because of ban')
                    client.close()
                    stop_thread = True
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
        if stop_thread:
            break

        message = input('')
        full_message = f'{nickname}: {message}'

        if message.startswith('/'):
            if nickname == 'admin':
                if message.startswith('/kick '):
                    client.send(f'KICK {message[6:]}'.encode('ascii'))
                elif message.startswith('/ban '):
                    client.send(f'BAN {message[5:]}'.encode('ascii'))
                else:
                    print('Unknown command or syntax error.')
            else:
                print('Commands can only be executed by an administrator.')
        else:
            client.send(full_message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()