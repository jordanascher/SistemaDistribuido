from socket import *
from threading import Thread

myHost = "localhost"
myPort = 50008

socketClient = socket(AF_INET, SOCK_STREAM)

def conecta ():
    print('Conectando ao servidor...')
    socketClient.connect((myHost, myPort))
    msgRcv = socketClient.recv(1024).decode('utf-8')
    print(msgRcv)

def desconecta ():
    socketClient.close()
    print('Saindo do chat...')

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

# thread for each roda ao mesmo tempo com o cliente escrita e de leitura que funcionam paralamente
def main():
    conecta()
    thread1 = Thread(target=enviarMensagem)
    thread1.start()

main()