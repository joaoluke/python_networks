# python_networks

## Client_TCP

Para enviar alguns dados lixos afim de testar, fazer fuzzing ou qualquer outra tarefa, devemos ter um Cliente TCP de um forma simples

- Importo a biblioteca socket para usarmos socketes bloqueantes.
- Defino meu host e porta a serem conectados.
- Crio um objeto socket com parametro AF_INET que me diz que queremos um endereço IPv4 padrão ou um nome host e o SOCK_STREAM que indica que esse será um cliente TCP.
- Envio alguns dados a ele.
- Recebo alguns dados.

Obs.: fazendo algumas suposições sérias sobres os sockets em relação aos quais você deveria estar ciente. A primeira suposição é que nossa conexão sempre terá sucesso e a segunda é que o servidor sempre estará esperando que lhe enviemos dados antes (em oposição aos servidores que esperam enviar dados a você antes e esperam a sua resposta), a terceira suposição é de que o servidor sempre enviará dados de volta imediatamente.

## Contributing
Os comentários e os códigos foram retirados do livro: Black Hat Python de Justin Seitz publicado pela editora Novatas. Com algumas alterações quando aos comentários e ao código adaptado a versão 3.9 do Python
