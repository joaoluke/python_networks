# python_networks

<details open="open">
  <summary>Sumario</summary>
  <ol>
    <li>
      <a href="#about-the-project">Sobre o projeto</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Questões Iniciais</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#client-tcp">Cliente TCP</a></li>
    <li><a href="#client-udp">Cliente UDP</a></li>
    <li><a href="#server-tcp">Server TCP</a></li>
    <li><a href="#contributing">Contribuição</a></li>
    <li><a href="#contact">Contato</a></li>
  </ol>
</details>

## Client TCP

Para enviar alguns dados lixos afim de testar, fazer fuzzing ou qualquer outra tarefa, devemos ter um Cliente TCP de um forma simples

- Importo a biblioteca socket para usarmos socketes bloqueantes.
- Defino meu host e porta a serem conectados.
- Crio um objeto socket com parametro `AF_INET` que me diz que queremos um endereço IPv4 padrão ou um nome host e o `SOCK_STREAM` que indica que esse será um cliente TCP.
- Envio alguns dados a ele.
- Recebo alguns dados.

Obs.: fazendo algumas suposições sérias sobres os sockets em relação aos quais você deveria estar ciente. A primeira suposição é que nossa conexão sempre terá sucesso e a segunda é que o servidor sempre estará esperando que lhe enviemos dados antes (em oposição aos servidores que esperam enviar dados a você antes e esperam a sua resposta), a terceira suposição é de que o servidor sempre enviará dados de volta imediatamente.

## Client UDP

Não sendo muito diferente do client TCP, fazemos apenas quatro pequenas alterações para que os pacotes sejam enviados em formato UDP:

```python
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```
- Onde `SOCK_DGRAM` indicando um cliente UDP.
- Fazemos um `blind()` para conectar o socket ao esdereço de destino.
- E o `sendto()` passamos os dados e o servidor para qual voce deseja enviar os dados.
- O ultimo passo consiste em chamar o `recvfrom()`para receber de volta os dados UDP.

Obs.: como o protocolo UDP não é orientado a conexão, não há nenhuma chamada anterior a `connect()`. Você Irá observar que quanto os dados quanto os detalhes sobre o host remoto e a porta são recebidos, juntamente com a mensagem UDP que no nosso caso foi `Hello, server UDP`.

Para mais informações sobre a conexão UDP com Python veja o link [UDP exemple](https://pythontic.com/modules/socket/udp-client-server-example)

## Server TCP

Criar um servidor TCP é tão simples quando criar um cliente, porém é necessário atenção para configurar seu server ao seu client, talvez pode dar erros de conexão, pois você pode estar tentando fazer essa conexão em portas reservadas. Preste atenção!

Eis um servidor TCP multithreaded padrão:

- No começo fazemos o que já estamos acostumados a fazer com o `bind()` passando o endereço IP e a porta que queremos que o servidor fique ouvindo.
- Depois com o `server.listen(1)` dizemos ao servidor para começar a ouvir com o máximo de conexões definidas em 1 (opção minha, você pode por quantas você quiser)
- Então com a função `handle_client()` o servidor entra em seu laço principal, em que aguarda uma conexão de entrada.
- Quando o cliente se conecta, recebemos o socket do cliente na variável `client`e os detalhes da conexão remota remota numa variável em `addr` em `client, addr = server.accept()`
- Em seguida criamos um novo objeto thread que aponta para nossa função `handle_client()` e passamos o objeto socket referente ao cliente como argumento `client`
- Iniciamos a thread para que cuide da conexão com o cliente e o laço principal do nosso servidor estará pronto para cuidar de outra conexão de entrada em `client_handler.start()`
- A função `client_handler()` executa `recv()` e, em seguida, envia uma mensagem simples ao cliente "ARK!"

Para mais informações sobre a conexão entre servidor TCP e cliente TCP com Python veja o link [TCP conection exemple](https://pymotw.com/3/socket/tcp.html)

## Contributing
Os comentários e os códigos foram retirados do livro: Black Hat Python de Justin Seitz publicado pela editora Novatec. Com algumas alterações quando aos comentários e ao código adaptado a versão 3.9 do Python

## Contact

Me mande uma mensagem caso tenha duvidas

João Lucas

[@Instagram](https://www.instagram.com/joaolucas.deoliveira56/) - joaolucas.deoliveira56

[@Linkedin](https://www.linkedin.com/in/joaolucasdeoliveira56/) - joaolucasdeoliveira56/
