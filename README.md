# python_networks

*Client_TCP

Para enviar alguns dados lixos afim de testar, fazer fuzzing ou qualquer outra tarefa, devemos ter um Cliente TCP de um forma simples

1- Importo a biblioteca socket para usarmos socketes bloqueantes
2- Defino meu host e porta a serem conectados
3- Crio um objeto socket com parametro AF_INET que me diz que queremos um endereço IPv4 padrão ou um nome host e o SOCK_STREAM que indica que esse será um cliente TCP
4- Envio alguns dados a ele
5- Recebo alguns dados
