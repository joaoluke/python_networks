# python_networks

*Client_TCP

Para enviar alguns dados lixos afim de testar, fazer fuzzing ou qualquer outra tarefa, devemos ter um Cliente TCP de um forma simples

- Importo a biblioteca socket para usarmos socketes bloqueantes.
- Defino meu host e porta a serem conectados.
- Crio um objeto socket com parametro AF_INET que me diz que queremos um endereço IPv4 padrão ou um nome host e o SOCK_STREAM que indica que esse será um cliente TCP.
- Envio alguns dados a ele.
- Recebo alguns dados.
