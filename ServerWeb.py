#!/src/bin/env python
import socket
import os
from threading import Thread

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 5001)) #definição do servidor
server_socket.listen(5) #quantidade de conexões


#******************************CLASSE DE THREAD COM CLIENTE
class Client(Thread): #cada instância dessa classe possui um processo em execução para um único cliente
    #herança da classe Thread
    def __init__(self,socket_client,ip_Adress):   #método construtor da classe
        Thread.__init__(self)
        self.lista = ["GET", "HEAD", "POST", "LIST"]
        self.socket_client = socket_client
        self.ip_Adress = ip_Adress 
        print("[Conexão estabelecida com:", adress,"]")

    def run(self):#método é executado ao fazermos Thread.start()
        self.socket_client.setblocking(True)
        
        while True:
            
            try: #caso o socket esteja aberto
                msg = self.socket_client.recv(4096)   
                data = msg.decode().split(" ") #só sei que foi assim
            except:
                print("[Conexão encerrada com:", adress,"]") #socket está fechado
                break   
            resposta , arq = self.response(data) #recebe corpo response e arquivo requisitado
            self.socket_client.sendall(resposta.encode())
            if(arq!=None):
                self.socket_client.sendall(arq)       
            self.socket_client.close()
            
    def response(self,dado):
        if(dado[0] in self.lista): #se a string estiver no array
            if(dado[0]=="GET"):
                return self.get(dado[1:]) #lista a partir do índice 1 em diante
            elif(dado[0]=="HEAD"):
                return self.head(dado[1:],False) #False: não enviarei nenhum arquivo
            elif(dado[0]=="POST"):
                return self.post(dado[1:])  #Cliente deseja enviar algum arquivo!  
            elif(dado[0]=="LIST"):
                print("LIST")
                return self.listar(dado[1:])

            return ("HTTP/1.1 405 Method Not Allowed\r\n\r\n", None)
        else:
            return ("HTTP/1.1 405 Method Not Allowed\r\n\r\n", None)

    def get(self, dado):
        response, readFile = self.head(dado, True) #recebe cabeçalho do response e arquivo requisitado.
                                                    #True: quero receber arquivo se ele existir
        if(readFile!=None): #verifica se path contém / no início (fatiamento de string)
            diretorio = str.rpartition(dado[0].replace("%",""), ".")#cria lista com diretório do arquivo e extensão
            print("[Arquivo solicitado:", dado[0], "]")
            if(diretorio[2].find("html")==-1):
                return (response, readFile) #envio de response e arquivo solicitado     
            else:
                response = response + readFile.decode("utf-8") 
                return (response, None) #página enviada no corpo response
        return ("HTTP/1.1 404 Bad Request - File not found\r\n\r\n", None)

    def head(self, dado, flag):
        #método retorna cabeçalho de requisição e arquivo solicitado
        diretorio = str.rpartition(dado[0], ".")#cria lista com diretório do arquivo e extensão
        dado[0] = dado[0].replace("%20", " ", len(dado[0]))
        if(dado[0][0]=="/"): #verifica se path contém / no início (fatiamento de string)
            if(len(dado[0])==1):#retornar index.html da raiz do servidor
                try:
                    arquivo = open('index.html', 'rb').read()
                except:
                    return ("HTTP/1.1 404 Bad Request - File not found\r\n\r\n", None)
            else: 
                try:#leitura de um arquivo qualquer
                    diretorio = str.rpartition(dado[0].replace("%",""), ".")
                    arquivo = open(diretorio[0][1:] + "." + diretorio[2], 'rb').read()
                except:
                    return ("HTTP/1.1 404 Bad Request - File not found\r\n\r\n", None)

            if(arquivo!=None):
                response = "HTTP/1.1 200 OK\r\n" + "Connection: close\r\n" + \
                    "Content Lenght:" + str(len(arquivo)) + "\r\nContent Type:" + \
                        diretorio[1] + diretorio[2] + "\r\n\r\n"
                if flag:
                    return (response, arquivo) #retorno response e arquivo lido
                else:
                    return (response, None) #retorno apenas response              
            else:
                return ("HTTP/1.1 404 Bad Request - File not found\r\n\r\n", None)
        return ("HTTP/1.1 400 Bad Request - File not found\r\n\r\n", None)
    
    def post(self, dado):
        if(dado[0][0]=="/"): #verifica se path contém / no início (fatiamento de string)
            #verificar se arquivo já existe no servidor, caso não, continuar
            if not os.path.exists(os.getcwd() +"/Musicas"):#cria diretório 'musica' caso ainda não exista
                os.mkdir(os.getcwd() +"/Musicas")

            dado[0] = dado[0].replace("%20", " ", len(dado[0]))

            if(".mp3" in dado[0]):
                arquivo = open(os.getcwd() + "/Musicas" + dado[0], 'wb')
                print("Arquivo com extensão mp3")
            else:
                arquivo = open(os.getcwd() + "/Musicas" + dado[0] + ".mp3", 'wb')

            while True:
                try:
                    self.socket_client.settimeout(10.0)
                    msg = self.socket_client.recv(4096)
                    print("Recebendo música")
                except:
                    return ("HTTP/1.1 404 - Any error ocurred", None) #alguma falha ocorreu
                arquivo.write(msg)#adicionar bits recebidos referente à musica em recepção
                #self.socket_client.close()
            arquivo.close()
            print("Arquivo enviado")
            return ("HTTP/1.1 200 - File reiceived", None)
                       
        return ("HTTP/1.1 404 - Any error ocurred", None) #falha no envio



    def listar(self, dado):
        if(dado[0][0]=="/"):
            #listinha =  str(os.listdir(os.getcwd() +"/Musicas"))[1:-1] #obtem todos os arquivos do diretório
            listinha = os.listdir(os.getcwd() +"/Musicas")
            for musica in listinha:
                if(".mp3" not in musica):
                    listinha.remove(musica)
            listinha = str(listinha)[1:-1] #lista somente com as músicas em mp3
            return  ("HTTP/1.1 200 OK\r\n" + "Connection: close\r\n" + \
                    "Content Lenght: 0" + str(len(listinha)) + "\r\nContent Type:" + \
                        "text" + "\r\n\r\n", listinha.encode())
        

print('[Iniciado]')
while True:
    print("[Aguardando conexão]\n")
    connection, adress  = server_socket.accept() #retorna socket de conexão realizado e endereço do usuário
    newProcess = Client(connection, adress) #é criada instância de novo processo
    newProcess.start() #inicia thread de conexão recebida
server_socket.close()
