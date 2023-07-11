from socket import *
import socketserver
from datetime import datetime
from threading import *

host = 'localhost'
port = 50007
#array que vai armazena cada cliente que entra
connectionClientes = []
#get pega a posição do array do cliente e o pop vai remover
def deletarCliente(cliente):
    posicao = getPosicaoCliente(cliente)
    connectionClientes.pop(posicao)
#append vai inserir na lista de clientes
def inserirCliente(cliente):
    connectionClientes.append(cliente)
    return getPosicaoCliente(cliente)
#ele vai pegar posição que o cliente esta no array 
def getPosicaoCliente(cliente):
    i = 0
    posicaoCliente = None

    for connectionCliente in connectionClientes:
        if (len(connectionCliente) > 0 and connectionCliente['ip'] == cliente['ip'] and connectionCliente['port'] == cliente['port']):
            posicaoCliente = i
            break

        i = i + 1

    return posicaoCliente
#formata cliente é só para exibir ele
def formataCliente(posicao, cliente):
    return 'Cliente '+str(posicao+1) + '-' + str(cliente['ip']) + ':' + str(cliente['port'])
#tupla posição 0 é o enderenço e a um é a porta
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
            msgServidor = 'Servidor diz: Mensagem recebida'
            connection.send(msgServidor.encode('utf-8'))

def main():
    socketServer = socket(AF_INET, SOCK_STREAM)
    # bind ele vai associar um endereço local a um soquete servidor 
    socketServer.bind((host, port))
    print("Iniciando servidor...")
    #aguardar a requisição do cliente 
    socketServer.listen()

    while True:
        connection, address = socketServer.accept()
        # msgServidor = 'Servidor aceitou a conexão'
        # connection.send(msgServidor.encode('utf-8'))
        # thread vai receber a função recebe clientes, ele vai receber o endereço do accept do socket,o servidor vai receber do cliente sempre que ele recebe uma msg.
        thread = Thread(target=recebeCliente, args=(connection, address))
        thread.start()

main()