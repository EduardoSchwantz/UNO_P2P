# 🃏 Jogo UNO em Arquitetura P2P (TCP Socket)

Este projeto implementa uma versão simplificada do jogo UNO, com comunicação entre múltiplos jogadores via sockets TCP e arquitetura **peer-to-peer (P2P)**. O jogo permite que cada peer atue como jogador e servidor ao mesmo tempo.

Esse projeto foi desenvolvimento em conjunto com os colegas:

Isabele Santos Scherdien

Thiago Dias Mazzoni

Diciplina de Redes de Computadores

Administrada pelo Professor Dr.GUILHERME RIBEIRO CORRÊA

---

## 🚀 Requisitos

- Python 3.7+
- Sistema operacional: Windows ou Linux (funciona em ambos)
- Conexão entre os peers permitida pela rede/firewall

---

## 🔓 Liberação da Porta 5000 (Firewall)

> A porta TCP `5000` é usada para comunicação entre peers.

### ▶️ No Windows:

1. Abra o PowerShell como Administrador
2. Execute:
   ```powershell
   New-NetFirewallRule -DisplayName "UNO P2P TCP 5000" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
### ▶️ No Ubuntu/Linux:
   ```
   sudo ufw allow 5000/tcp
   ```
Verifique se o ufw está ativo com:
   ```
  sudo ufw status
   ```
## 📥 Instalação

Clone o projeto ou copie os arquivos:


```
   git clone https://github.com/seu-usuario/uno-p2p.git
```
```
   cd uno-p2p
```

### ▶️Certifique-se de ter os seguintes arquivos no mesmo diretório:
   
   >main.py
   
   >peer.py
   
   >protocol.py
   
   >utils.py

### ▶️ Como Executar o Jogo
Cada jogador deve executar o jogo em uma máquina diferente ou em diferentes terminais com IPs distintos.

Para descobrir o ip da máquina utilize:

### ▶️ No Ubuntu/Linux:

   ``` ip```

### ▶️ No Windows:

   ``` ipconfig```

## 🔹 Passo 1: Executar o primeiro peer (host)
```Powershell
   python main.py
```
   >Digite seu nome (ex: Alice)

   >Escolha o host de escuta (0.0.0.0 ou localhost)

   >Escolha a porta: 5000


## 🔹 Passo 2: Executar o segundo peer
No segundo computador ou terminal:
>Digite seu nome (ex: Bob)

   >Host de escuta: 0.0.0.0

   >Porta: 5001, 5002 ou outra (diferente da primeira)

   >Em seguida, escolha a opção 1. Conectar a outro peer

   >Informe o IP do primeiro peer e a porta 5000

## 🎮 Menu do Jogo
Após inicializar, o jogo oferece este menu:

## === MENU ===
1. Conectar a outro peer
2. Ver mão de cartas
3. Jogar carta
4. Comprar carta
5. Enviar mensagem de chat
6. Sair

>Use 1 para conectar a novos peers

>Use 2 para ver todas cartas que você tem em mão

>Use 3 para jogar uma carta válida (baseada na do topo)

>Use 4 para comprar uma carta caso não tenha jogada válida

>Use 5 para conversar com os demais jogadores

>Use 6 para encerrar o programa

## 📡 Comunicação
O jogo utiliza TCP sockets com troca de mensagens codificadas em JSON

Mensagens são enviadas entre todos os peers conectados, sem servidor central

## 🛠 Problemas comuns
| Erro             | Possível causa                          | Solução                                                |
| ---------------- | --------------------------------------- | ------------------------------------------------------ |
| Conexão recusada | IP ou porta incorretos                  | Verifique se o peer está ativo e com firewall liberado |
| Não é sua vez    | Tentando jogar fora do turno            | Espere sua vez de jogar                                |
| Peer não aparece | Conexão TCP falhou ou não foi propagada | Verifique conexão e tente reconectar                   |
