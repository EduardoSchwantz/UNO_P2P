# 🃏 Jogo UNO em Arquitetura P2P (TCP Socket)

Este projeto implementa uma versão simplificada do jogo UNO, com comunicação entre múltiplos jogadores via sockets TCP e arquitetura **peer-to-peer (P2P)**. O jogo permite que cada peer atue como jogador e servidor ao mesmo tempo.
Esse projeto foi desenvolvimento em conjunto com os colegas Isabele Santos Scherdien e Thiago Dias Mazzoni para a diciplina de Redes de Computadores Administrada pelo Professor Dr.GUILHERME RIBEIRO CORRÊA
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
#No Ubuntu/Linux:
sudo ufw allow 5000/tcp

Verifique se o ufw está ativo com:
sudo ufw status
