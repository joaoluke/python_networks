[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
<img alt="GitHub" src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white"/>
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Python Networks</h1>

  <p align="center">
    Programação Python em Redes para dev's, hackers e pentesters.
    <br />
    <br />
    ·
    <a href="https://github.com/joaoluke/python_networks/issues">Reportar Bug</a>
    ·
    <a href="https://github.com/joaoluke/python_networks/issues">Solicitar Recurso</a>
  </p>
</p>

<details open="open">
  <summary>Sumário</summary>
  <ol>
    <li>
      <a href="#o-projeto">Sobre o projeto</a>
    </li>
    <li>
      <a href="#getting-started">Questões Iniciais</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Instalações</a></li>
      </ul>
    </li>
    <li><a href="#client-tcp">Cliente TCP</a></li>
    <li><a href="#client-udp">Cliente UDP</a></li>
    <li><a href="#server-tcp">Server TCP</a></li>
    <li><a href="#netcat">Substituindo o Netcat</a></li>
    <li><a href="#contributing">Contribuição</a></li>
    <li><a href="#contato">Contato</a></li>
    <li><a href="#reconhecimentos">Reconhecimentos</a></li>
  </ol>
</details>

## O Projeto

Python é a linguagem "queridinha", para os amantes de cibersegurança, e como vamos explorar o conteúdo de um dos maiores best-sellers do assunto (**Black Hat Python**) vamos aprender a fundo sobres as tecnologias e até mesmo construir nossas próprias ferramentas para pentest com Python!

Vamos aprender sobre o capítulo 2, 3 e 4 de Black Hat onde se aborda temas de rede, vamos aprender fazer nosso próprio cliente TCP, UDP, server TCP, vamos fazer um substituto do Netcat, um Proxy, tutelamento SSH, Decodificando a camada IP, Roubando credenciais de emails, Sniffing e muito mais (vamos deixar de ser apenas um "script kiddies"). Então senta confortavelmente e vamos ao haking!

Se você ama programação, ama Python, ama cibersegurança esse conteúdo é para você! Fiz com todo carinho para você <3.

## Questões Iniciais

Vamos dar inicio a preparação do ambiente para programarmos, para inicio tenha um computador com acesso a internet, um editor de texto ou IDE (meu conselho é usar o PyCharm versão gratuita), o livro pede para que você instale o Kali Linux em um VM, mas pode ser em qualquer maquina Linux ou até mesmo MacOS, se precisarmos de algum tipo de instalação de pacote vou citar em cada capitulo, fique tranquilo!

Minhas dicas são: pratique cada tema muito, veja bem os exemplos e as referencias externas que irei colocar em cada assunto, busque informações do tema discutido pela internet, se caso tiver alguma duvida específica pode-me mandar por contato ou por no StackOverflow, espero que você tenha curiosidade e comprometimento para absolver cada tópico a fundo, se a principio um exemplo parecer muito difícil, calma e olhe com cuida e sem pressa, pois eu vou comentar cada tópico passo a passo.

### Pré-requisitos

- Maquina Linux (seja VM ou instalada no HD)
- Conhecimento prévio em Python (não vou entrar em detalhes da sintaxe e sim das funcionalidades, então é bom você ter um conhecimento intermediário de lógica de programação e de Python)
- Kali-Linux (opcional)
- Conhecimento de comandos linux
- Python3 instalado em sua máquina (de preferência ser padrão no sistema todo)
- WingIDE (opcional, sugestão do livro)
- Conhecimento básico em redes de computadores (saber como funciona os protocolos podem lhe ajudar muito nessa demo)

Obs.: Coloquei alguns links bacana no Reconhecimento no final do arquivo com alguns conteudo bacana de Redes, comando linux, instalação do PyCharm...

### Instalações

Para instalar o `pip` pra podermos instalar algumas ferramentas que vamos usar use o seguinte comando:

```cmd
sudo apt-get install python-setuptools python-pip
```

Para instalar o Python 3 primeiro verifique se tem alguma versão do Python instalada em sua maquina com o comando:

```cmd
$ which python
```

ou

```cmd
$ which python3
```

que deve retornar algo como `/usr/bin/python`. Isso significa que o Python está instalado nesse endereço.

Para instala-lo com apt-get:

```cmd
$ sudo apt-get install python3
```

```cmd
$ sudo apt-get install python3-pip
```

Para instalar o WingIDE use o comando:

```cmd
$ sudo dpkg -i wingide5_5.0.9-1_i386.deb
```

e

```cmd
$ sudo apt-get -f install
```

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

Obs.: É isso, esses códigos serão estendidos (em novos arquivos, para não atrapalhar o versionamento) nas próximas seções, em que desenvolveremos um substituto para o Netcat e um Proxy TCP! Então borá lá!

## Netcat

Chegou a hora de criarmos o nosso próprio canivete suíço das redes: O NETCAT. Muitas das vezes os administradores de rede "espertinhos" removem ele do sistema, mas o python está presente nos servidores.

Então para estes caso é muito útil criar um cliente e servidor simples para rede que possam ser usados para enviar arquivos ou ter um listener (processo que verifica se há solicitações de conexão) que possibilite o acesso

Se você invadiu um sistema web, certamente deveria deixar uma callback Python para ter acesso secundário antes de lançar mão do uso de um de seus cavalos de Tróia ou de suas backdoors (portas dos fundos).

1 - Então vamos começar com nosso Netcat: Calma! O arquivo é grande, eu sei! Mas vamos por partes, vou começar explicando desde o começo:

- Primeiro faço algumas importações
- Depois defino algumas variáveis globais.
- Ai cria a função principal `def usage():`, ela será responsável pelo tratamento dos argumentos da linha de comando pela chamada do restante das funções.

Começando lendo todas as opções de linha de comando:

``` python
try:
opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
["help", "listen", "execute=", "target=", "port=", "command", "upload="])
except getopt.GetoptError as err:
logging.error("%s", err)
usage()
```
e definindo as variáveis necessárias de acordo com as opções detectadas. E se alguma informação de comando não atender nossos critérios, vamos exibir informações sobre como usar o script de acordo com nossa função `usage()`.
E aqui tentamos imitar o netcat e enviar dados de stdin pela rede:
```python
f not listen and len(target) and port > 0:
buffer = sys.stdin.read()

client_sender(buffer)
```
E por fim detectamos que é necessário configurar um socket para ouvir a rede e processamos comandos adicionais: `server_loop()` onde carregamos um arquivo, executamos um comando, iniciamos um schell de comandos.

2 - A partir de agora vamos falar da segunda parte do nosso script `def client_sender():`, já estou achando que você está se familiarizando com tudo isso.

- Começamos a criar nosso objeto socket TCP e depois testamos ele.
- Depois o testamos para saber se recebemos algum dado de entrada de stdin.
```python
if len(buffer):
client.send(buffer)
while True:
...
```
- Se tudo estiver ok, enviaremos os dados remotamente e receberemos dados de volta (`while recv_len:`)
- Então preparamos mais dados de entrada (`buffer = input('')`) do usuário e continuaremos a enviar e receber dados até o usuário encerrar nosso script.

3 - Agora vamos criar o laço principal do nosso servidor, além de uma função stub que cuidará tanto da execução do nosso comando quanto do nosso shell de comandos completo.

Bom a essa altura do campeonato você já deve estar bem familiarizado em criar um servidor TCP completo com threading, então não vamos entrar em detalhes da nossa função `server_loop():`

- Algo que tem na função `run_command():` que ainda não falamos sobre é a subprocess, que é uma biblioteca que provê uma interface eficaz para criar processos, proporcionando diversas maneiras de iniciar e interagir com programas clientes.
- Aqui `output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)` simplesmente executamos qualquer comando que seja passado, executando no sistema operacional e retornando a saída do comando ao cliente que se conectou a nós.

4 - Por fim vamos implementar a lógica para fazer upload de arquivos, executar comando e implementar o nosso shell: `client_handler():`

- Nessa primeira porção de código (`if len(upload_destination):`) é responsável por determinar se nossa ferramenta de rede está configurada para receber um arquivo quando uma conexão for estabelecida.
- Inicialmente, recebemos os dados de arquivo em um laço (`while True:
data = client_socket.recv(1024)`) para garantir que recebemos tudo.
- Depois, processamos nossa funcionalidade de execução, que chamamos nossa função `run_command()` e simplesmente envia o resultado de volta pela rede.
- Por fim de tudo temos o código que cuida de nosso shell de comandos, ele contínua a executar comandos à medida que os enviamos e a saída é mantida de volta.

## Contributing
Os comentários e os códigos foram retirados do livro: Black Hat Python de Justin Seitz publicado pela editora Novatec. Com algumas alterações quando aos comentários e ao código adaptado a versão 3.9 do Python

## Contato

Me mande uma mensagem caso tenha duvidas

João Lucas

[@Instagram](https://www.instagram.com/joaolucas.deoliveira56/) - joaolucas.deoliveira56

[@Linkedin](https://www.linkedin.com/in/joaolucasdeoliveira56/) - joaolucasdeoliveira56/

## Reconhecimentos

* [ProgrammerSought](https://www.programmersought.com/)
* [HOWTO sobre a Programação de Soquetes](https://docs.python.org/pt-br/3/howto/sockets.html)
* [Instalação do Pycharm](http://pythonclub.com.br/instalando-pycharm-ubuntu.html)
* [Kali-Linux em Virtual Box](https://www.kali.org/docs/virtualization/install-virtualbox-guest-vm/)
* [Comandos Linux](https://www.linuxpro.com.br/dl/guia_500_comandos_Linux.pdf)
* [Guia Básico de Redes](https://www.algosobre.com.br/informatica/redes-de-computadores-nocoes-basicas.html)

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/joaoluke/python_networks/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/joaoluke/python_networks/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/joaoluke/python_networks/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[product-screenshot]: images/screenshot.png
