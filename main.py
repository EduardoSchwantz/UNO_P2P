import time
from peer import Peer
from utils import Card

def show_hand(peer):
    if not peer.game_state:
        print("Jogo ainda não começou ou estado indisponível.")
        return
    print(f"\nCarta no topo da mesa: {peer.game_state.top_card}\n")
    hand = peer.game_state.players.get(peer.name, [])
    print("Sua mão:")
    for i, card in enumerate(hand):
        print(f"{i + 1}. {card}")
    print()

def play_card(peer):
    if not peer.game_state:
        print("Estado do jogo ainda não disponível.")
        return

    if peer.game_state.current_turn != peer.name:
        print("Não é sua vez.")
        return

    show_hand(peer)
    try:
        choice = int(input("Escolha o número da carta que deseja jogar: ")) - 1
        hand = peer.game_state.players[peer.name]
        if 0 <= choice < len(hand):
            card = hand[choice]
            if card.is_playable_on(peer.game_state.top_card):
                payload = {"card": card.to_dict()}
                if card.value in ["wild", "+4"]:
                    cor = input("Escolha a cor para o coringa (red, yellow, green, blue): ").strip().lower()
                    if cor not in ["red", "yellow", "green", "blue"]:
                        print("Cor inválida. Jogada cancelada.")
                        return
                    payload["color"] = cor
                peer.send_message_to_all("PLAY_CARD", payload)
            else:
                print("Essa carta não pode ser jogada.")
        else:
            print("Escolha inválida.")
    except Exception as e:
        print(f"Erro: {e}")
        
def buy_card(peer):
    if not peer.game_state:
        print("Estado do jogo ainda não disponível.")
        return
    if peer.game_state.current_turn != peer.name:
        print("Não é sua vez.")
        return
    peer.send_message_to_all("BUY_CARD", {})

def main():
    name = input("Digite seu nome: ")
    listen_host = input("Digite o host de escuta (ex: 0.0.0.0 para todos ou localhost): ").strip()
    if listen_host == "":
        listen_host = "0.0.0.0"
    port = int(input("Digite sua porta de escuta (ex: 5000): "))
    
    peer = Peer(name, host=listen_host, port=port)
    peer.start()

    while True:
        print("\n=== MENU ===")
        print("1. Conectar a outro peer")
        print("2. Ver mão de cartas")
        print("3. Jogar carta")
        print("4. Comprar carta")
        print("5. Enviar mensagem de chat")
        print("6. Sair")

        choice = input("Escolha: ")

        if choice == "1":
            host = input("Host do peer (IP do outro computador): ").strip()
            port = int(input("Porta: "))
            peer.connect_to_peer(host, port)
        elif choice == "2":
            show_hand(peer)
        elif choice == "3":
            play_card(peer)
        elif choice == "4":
            buy_card(peer)
        elif choice == "5":
            msg = input("Digite a mensagem: ")
            peer.send_message_to_all("CHAT_MSG", {"message": msg})
        elif choice == "6":
            print("Encerrando jogo.")
            break
        else:
            print("Opção inválida.")

        time.sleep(1)

if __name__ == "__main__":
    main()
