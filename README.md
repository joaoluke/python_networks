# python_networks

## Client_TCP

Para enviar alguns dados lixos afim de testar, fazer fuzzing ou qualquer outra tarefa, devemos ter um Cliente TCP de um forma simples

- Importo a biblioteca socket para usarmos socketes bloqueantes.
- Defino meu host e porta a serem conectados.
- Crio um objeto socket com parametro `AF_INET` que me diz que queremos um endereço IPv4 padrão ou um nome host e o `SOCK_STREAM` que indica que esse será um cliente TCP.
- Envio alguns dados a ele.
- Recebo alguns dados.

Obs.: fazendo algumas suposições sérias sobres os sockets em relação aos quais você deveria estar ciente. A primeira suposição é que nossa conexão sempre terá sucesso e a segunda é que o servidor sempre estará esperando que lhe enviemos dados antes (em oposição aos servidores que esperam enviar dados a você antes e esperam a sua resposta), a terceira suposição é de que o servidor sempre enviará dados de volta imediatamente.

## Client_UDP

Não sendo muito diferente do client TCP, fazemos apenas quatro pequenas alterações para que os pacotes sejam enviados em formato UDP:

```python
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```
- Onde `SOCK_DGRAM` indicando um cliente UDP.
- Fazemos um `blind()` para conectar o socket ao esdereço de destino.
- E o `sendto()` passamos os dados e o servidor para qual voce deseja enviar os dados.
- O ultimo passo consiste em chamar o `recvfrom()`para receber de volta os dados UDP.

Obs.: como o protocolo UDP não é orientado a conexão, não há nenhuma chamda anterior a `connect()`. Voce Irá observar que quanto os dados quanto os detalhes sobre o host remoto e a porta são recebiddos, juntamente com a mensagem UDP que no nosso caso 

## Contributing
Os comentários e os códigos foram retirados do livro: Black Hat Python de Justin Seitz publicado pela editora Novatas. Com algumas alterações quando aos comentários e ao código adaptado a versão 3.9 do Python
