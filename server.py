
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
        
#handling client messages
def handle(client):
    while True:
        try:
            #broadcasting
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                
                if nicknames[clients.index(client)] == 'admin':
                    
                    name_to_kick = msg.decode('ascii')[5:]
                    #another option is reading the socket ip and doing ip bands
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            
            # insures parasing for ban is done right        
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    
                    # "a" is appending mode
                    with open('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                        
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
                
                # removing clients
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                # if need older py version compatiblilty use    '{} left!'.format(nickname)
                broadcast(f'{nickname} left!'.encode('ascii'))
                nicknames.remove(nickname)
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
           bans = f.readlines()
        
        # bans = [line.strip() for line in f]
        #     if nickname in bans:

       if nickname+'\n' in bans:
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