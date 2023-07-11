from socket import *
import socketserver
from datetime import datetime
from threading import *

host = 'localhost'
port = 50008

connectionClientes = []

def deletarCliente(cliente):
    posicao = getPosicaoCliente(cliente)
    connectionClientes.pop(posicao)

def inserirCliente(cliente):
    connectionClientes.append(cliente)
    return getPosicaoCliente(cliente)

def getPosicaoCliente(cliente):
    i = 0
    posicaoCliente = None

    for connectionCliente in connectionClientes:
        if (len(connectionCliente) > 0 and connectionCliente['ip'] == cliente['ip'] and connectionCliente['port'] == cliente['port']):
            posicaoCliente = i
            break

        i = i + 1

    return posicaoCliente

def formataCliente(posicao, cliente):
    return 'Cliente '+str(posicao+1) + '-' + str(cliente['ip']) + ':' + str(cliente['port'])

def recebeCliente(connection, address):
    while True:
        cliente = {
            'ip': address[0],
            'port': address[1]
        }
        
        posicao = getPosicaoCliente(cliente)

        if (posicao is None):
            posicao = inserirCliente(cliente)
            msgServidor = 'Conexão aceita pelo servidor'
            connection.send(msgServidor.encode('utf-8'))
            print(formataCliente(posicao, cliente) + ' solicitou conexão.')

        msgRcv = connection.recv(1024).decode('utf-8')
        currentDateAndTime = datetime.now()
        print(formataCliente(posicao, cliente))
        print(currentDateAndTime.strftime("%d/%b/%Y %H:%M:%S"))
        print(msgRcv)

        if (msgRcv == "sair"):
            deletarCliente(cliente)
            msgDesconecta = "Conexão encerrada"
            connection.send(msgDesconecta.encode("utf-8"))
            print(formataCliente(posicao, cliente) + ' desconectado.')
            connection.close()
            break
        else:
            msgServidor = 'Servidor diz: Mensagem recebida.'
            connection.send(msgServidor.encode('utf-8'))

def main():
    socketServer = socket(AF_INET, SOCK_STREAM)
    # bind ele vai associar um endereço local a um soquete
    socketServer.bind((host, port))
    print("Iniciando servidor...")
    socketServer.listen()

    while True:
        connection, address = socketServer.accept()
        # msgServidor = 'Servidor aceitou a conexão'
        # connection.send(msgServidor.encode('utf-8'))
        thread = Thread(target=recebeCliente, args=(connection, address))
        thread.start()

main()