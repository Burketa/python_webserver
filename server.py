import socket

# Definições gerais do programa (Debug).
#########################################
USE_LOCALHOST = True
PRINT_REQUEST = False
PRINT_FILENAME = False
#########################################

# Define a porta a ser escutada. (Padrão HTTP)
SERVER_PORT = 80

# Define se o servidor usará o localhost ou IP local.
if(USE_LOCALHOST):
    SERVER_HOST = 'localhost'
else:
    # 'socket.gethostbyname(socket.gethostname())'
    SERVER_HOST = 'IP DO SERVIDOR - PROVAVELMENTE 10.20.xx.xxx'

print('Usando o IP:\t' + SERVER_HOST)

# Criação e configuração do socket.
# Abre o socket configurado com o protocolo TCP.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Configura o socket para usar o mesmo socket, evitando erros devidos a recarregamentos muito rapidos da pagina.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Liga o processo ao IP do servidor e porta selecionada.
server_socket.bind((SERVER_HOST, SERVER_PORT))
# Começa a escutar conexões de clientes.
server_socket.listen(1)

while True:
    print('-------------------------------------------------')
    print('Servidor rodando.')
    print('Escutando requisições...')

    # Espera uma conexão de algum cliente.
    client_connection, client_address = server_socket.accept()

    # Recupera e imprime a requisição do cliente.
    request = client_connection.recv(1024).decode()

    if(PRINT_REQUEST):
        print('Request:\n' + request)

    # Processa a requisição HTTP
    headers = request.split('\n')
    filename = headers[0].split()[1]

    if(PRINT_FILENAME):
        print('Filename: ' + filename)

    # Recupera o arquivo requisitado pelo usuário.
    # Mostra a pagina 'index.html' com o código 200 caso o cliente não tenha especificado o arquivo.
    # Mostra a página de 'error.html' com o código 404 caso não exista o arquivo requisitado.
    if filename == '/':
        filename = '/index.html'

    try:
        file = open('website' + filename, encoding='utf-8', errors='ignore')
        content = file.read()
        file.close()
        response = 'HTTP/1.1 200 OK\n\n' + content

    except FileNotFoundError:
        error_file = open('website/error.html',
                          encoding='utf-8', errors='ignore')
        error_content = error_file.read()
        error_file.close()
        response = 'HTTP/1.1 404 NOT FOUND\n\n' + error_content

    # Envia a resposta HTTP + o conteúdo da página recuperada acima.
    client_connection.sendall(response.encode())
    print('\nResposta enviada.')
    # Encerra a conexão com o servidor
    client_connection.close()
    print('\nConexão encerrada.')

# Fecha o socket.
server_socket.close()
