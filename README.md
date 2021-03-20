[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Python Networks</h1>

  <p align="center">
    Programação em Redes Python para dev's, hackers e pentesters.
    <br />
    <br />
    ·
    <a href="https://github.com/joaoluke/python_networks/issues">Reportar Bug</a>
    ·
    <a href="https://github.com/joaoluke/python_networks/issues">Solicitar Recurso</a>
  </p>
</p>

<details open="open">
  <summary>Sumario</summary>
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

Vamos aprender sobre o capítulo 2 de Black Hat onde se aborda temas de rede, vamos aprender fazer nosso próprio cliente TCP, UDP, server TCP, vamos fazer um substituto do Netcat, um Proxy, tutelamento SSH... (vamos deixar de ser apenas um "script kiddies"). Então senta confortavelmente e vamos ao haking!

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

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/joaoluke/python_networks/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/joaoluke/python_networks/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/joaoluke/python_networks/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
