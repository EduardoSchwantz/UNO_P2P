import socket
import threading
import json
from protocol import make_message, parse_message
from utils import GameState, Card

class Peer:
    def __init__(self, name, host='localhost', port=5000):
        self.name = name
        self.host = host
        self.port = port
        self.peers = [] 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_names = [self.name]
        self.game_state = None
        self.game_over = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"[{self.name}] Aguardando conexões em {self.host}:{self.port}...")
        threading.Thread(target=self.accept_peers, daemon=True).start()

    def accept_peers(self):
        while True:
            conn, addr = self.server_socket.accept()
            print(f"[{self.name}] Conexão recebida de {addr}")
            self.peers.append((conn, addr))
            #print(f"[{self.name}] Peers conectados agora: {[a for _, a in self.peers]}")
            threading.Thread(target=self.handle_peer, args=(conn,), daemon=True).start()

    def connect_to_peer(self, peer_host, peer_port):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((peer_host, peer_port))
            self.peers.append((conn, (peer_host, peer_port)))
            threading.Thread(target=self.handle_peer, args=(conn,), daemon=True).start()
            print(f"[{self.name}] Conectado a {peer_host}:{peer_port}")


            join_msg = make_message("JOIN_GAME", self.name, {"player_name": self.name})
            conn.sendall((join_msg + "\n").encode())

        except Exception as e:
            print(f"[{self.name}] Falha ao conectar: {e}")

    def handle_peer(self, conn):
        #print(f"[{self.name}] handle_peer iniciado para {conn}")
        buffer = ""
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        msg = parse_message(line)
                        self.handle_message(msg, conn)
            except Exception as e:
                print(f"Erro na comunicação: {e}")
                break

    def handle_message(self, msg, conn):
        msg_type = msg["type"]
        sender = msg["sender"]
        payload = msg["payload"]

        #print(f"[{self.name}] Recebido: {msg_type} de {sender}")

        if msg_type == "JOIN_GAME":
            player = payload["player_name"]
            if player not in self.player_names:
                self.player_names.append(player)
                #print(f"[{self.name}] {player} entrou no jogo.")

                for peer_conn, _ in self.peers:
                    if peer_conn != conn:
                        try:
                            peer_conn.sendall((json.dumps(msg) + "\n").encode())
                        except:
                            pass

            if self.name == self.player_names[0] and len(self.player_names) >= 2 and self.game_state is None:
                self.start_game()

        elif msg_type == "GAME_STATE":
            self.game_state = GameState.from_dict(payload)
            print(f"[{self.name}] Estado do jogo atualizado. Carta no topo: {self.game_state.top_card}")
            print(f"[{self.name}] É a vez de: {self.game_state.current_turn}")

            for player, hand in self.game_state.players.items():
                if len(hand) == 0:
                    self.game_over = True
                    print(f"[{self.name}] Jogo encerrado! {player} venceu!")
                    break

        elif msg_type == "PLAY_CARD":
            if self.game_over:
                print(f"[{self.name}] O jogo já acabou. Jogada ignorada.")
                return
            card_data = payload["card"]
            player = sender
            card = Card.from_dict(card_data)

            if self.game_state:
                if self.game_state.current_turn != player:
                    print(f"[{self.name}] Não é a vez de {player}. Jogada ignorada.")
                    return

                if not card.is_playable_on(self.game_state.top_card):
                    print(f"[{self.name}] {player} tentou jogar carta inválida: {card}")
                    return

                cor_coringa = payload.get("color")
                success = self.game_state.play_card(player, card, cor_coringa)

                if success:
                    print(f"[{self.name}] {player} jogou {card}")

                    for p, hand in self.game_state.players.items():
                        if len(hand) == 1:
                            self.send_message_to_all("CHAT_MSG", {"message": f"{p} está Gritando UNO!"})

                    over, winner = self.game_state.is_game_over()
                    if over:
                        self.game_over = True
                        self.send_message_to_all("CHAT_MSG", {"message": f"Jogo acabou! {winner} venceu!"})
                        self.broadcast_state()
                        return
                    else:
                        self.send_message_to_all("CHAT_MSG", {"message": f"É a vez de {self.game_state.current_turn}."})

                    self.broadcast_state()
                else:
                    print(f"[{self.name}] Jogada falhou: {card}")

            for peer_conn, _ in self.peers:
                if peer_conn != conn:
                    try:
                        peer_conn.sendall((json.dumps(msg) + "\n").encode())
                    except:
                        pass

        elif msg_type == "CHAT_MSG":
            print(f"{sender} diz: {payload['message']}")

            for peer_conn, _ in self.peers:
                if peer_conn != conn:
                    try:
                        peer_conn.sendall((json.dumps(msg) + "\n").encode())
                    except:
                        pass

        elif msg_type == "BUY_CARD":
            if self.game_over:
                print(f"[{self.name}] O jogo já acabou. Compra ignorada.")
                return
            player = sender
            if self.game_state and self.game_state.current_turn == player:
                drawn_cards = self.game_state.draw_cards(player, 1)
                if drawn_cards:
                    if player == self.name:
                        print(f"[{self.name}] Você comprou: {drawn_cards[0]}")
                    else:
                        print(f"[{self.name}] {player} comprou uma carta.")
                    self.send_message_to_all("CHAT_MSG", {
                        "message": f"{player} comprou uma carta."
                    })
                    self.broadcast_state()
                else:
                    print(f"[{self.name}] Não há cartas para comprar.")
            
            for peer_conn, _ in self.peers:
                if peer_conn != conn:
                    try:
                        peer_conn.sendall((json.dumps(msg) + "\n").encode())
                    except:
                        pass

    def send_message_to_all(self, msg_type, payload=None):
        #print(f"[{self.name}] Enviando '{msg_type}' para {[addr for _, addr in self.peers]}")
        msg = make_message(msg_type, self.name, payload)
        for conn, _ in self.peers:
            try:
                conn.sendall((msg + "\n").encode())
            except:
                pass

    def broadcast_state(self):
        if self.game_state:
            payload = self.game_state.to_dict()
            self.handle_message({
                "type": "GAME_STATE",
                "sender": self.name,
                "timestamp": "",
                "payload": payload
            }, None)
            self.send_message_to_all("GAME_STATE", payload)

    def start_game(self):
        self.game_state = GameState(self.player_names)
        self.game_state.start_game()
        self.broadcast_state()