
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
            message = client.recv(1024)
            broadcast(message)
        except:
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
       
       #request and store
       client.send("Sukana".encode('ascii'))
       nickname = client.recv(1024).decode('ascii')
       nicknames.append(nickname)
       clients.append(client)
       
       #print & broadcast
       print(f'Nickname is {nickname}')
       broadcast(f'{nickname} joined!'.encode('ascii'))
       client.send('Connected to server!'.encode('ascii'))
       
       #new THREAD for client
       thread = threading.Thread(target=handle, args=(client,))
       thread.start()
       
receive()