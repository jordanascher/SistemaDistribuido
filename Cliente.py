from socket import *
from threading import Thread

myHost = "localhost"
myPort = 50007
#socketClient cria um objeto  socket do cliente.
socketClient = socket(AF_INET, SOCK_STREAM)
# a função def conecta pelo localhost e porta 5007 ao servidor e manda uma msg conectando ao servidor
def conecta ():
    print('Conectando ao servidor...')
    socketClient.connect((myHost, myPort))
    msgRcv = socketClient.recv(1024).decode('utf-8')
    print(msgRcv)
# a função def desconecta e recebe um print saindo do chat quando desconecta e fecha o socket
def desconecta ():
    socketClient.close()
    print('Saindo do chat...')
#vai enviar msg o cliente envia para o servidor
def enviar(msg):
    socketClient.send(msg.encode('utf-8'))

def enviarMensagem():
    while True:
        msg = input('Cliente diz: ')
        enviar(msg)
        msgRcv = socketClient.recv(1024).decode('utf-8')
        print(msgRcv)
        if msg == 'sair':
            if (msgRcv == 'Conexão encerrada'):
                desconecta()
                break

# thread vai enviar a msg para o servidor
def main():
    conecta()
    thread1 = Thread(target=enviarMensagem)
    thread1.start()

main()