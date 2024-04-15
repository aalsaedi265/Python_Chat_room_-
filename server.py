
import socket
import threading

#connection
host = '127.0.0.1'
port = 55555

#start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) #binds to our host by passing tuple containing both values
server.listen()


# clients
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

def ban_user(name_to_ban):
    if name_to_ban in nicknames:
        name_index = nicknames.index(name_to_ban)
        client_to_ban = clients[name_index]
        clients.remove(client_to_ban)
        client_to_ban.send('You were banned by an admin.'.encode('ascii'))
        client_to_ban.close()
        nicknames.remove(name_to_ban)
        broadcast(f'{name_to_ban} was banned by an admin!'.encode('ascii'))

        with open('bans.txt', 'a') as f:
            f.write(f'{name_to_ban}\n')

def safely_remove_client(client):
    try:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames.pop(index)
        client.close()
        broadcast(f'{nickname} left!'.encode('ascii'))
    except ValueError:
        print("Client already removed")

        
#handling client messages
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = message[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            elif message.startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = message[4:]
                    ban_user(name_to_ban)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                broadcast(message.encode('ascii'))
        except Exception as e:
            print(f'Error handling message: {e}')
            safely_remove_client(client)
            break
        
# Receiving / Listening Function
def receive():
   while True:
       #accept connect
       client, address = server.accept() 
       print("Connected with {}".format(str(address)))
       
       #request
       client.send("NICKNAME".encode('ascii'))
       nickname = client.recv(1024).decode('ascii')
       
       with open('bans.txt', 'r') as f:
            bans = [line.strip() for line in f]
        
        # bans = [line.strip() for line in f]
        #     if nickname in bans:

       if nickname in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
       
       #admin password check
       if nickname == 'admin':
           client.send('PASSWORD'.encode('ascii'))
           password = client.recv(1024).decode('ascii')
           
           #real world need to be hashed in DB
           if password != 'atractivePW':
               client.send('REFUSE'.encode('ascii'))
               client.close()
               continue #this thread to connect and we have other threads to connect
                        # if fail will skip look for another 
               
       
       #store
       nicknames.append(nickname)
       clients.append(client)
       
       #print & broadcast
       print(f'Nickname is {nickname}')
       broadcast(f'{nickname} joined!'.encode('ascii'))
       client.send('Connected to server!'.encode('ascii'))
       
       #new THREAD for client
       thread = threading.Thread(target=handle, args=(client,))
       thread.start()
       
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('you were kicked by an admin'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))
        
       
receive()