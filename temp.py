import socket
import threading
import time

# Funzione per avviare il server
def start_server(host="127.0.0.1", port=65432):
    # Crea il socket del server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Ascolta un massimo di 1 connessione
    print(f"Server in ascolto su {host}:{port}...")

    conn, addr = server_socket.accept()  # Accetta la connessione
    print(f"Connesso da {addr}")
    while True:
        data = conn.recv(1024)  # Riceve i dati
        if not data:
            break
        print(f"Dati ricevuti: {data.decode('utf-8')}")
    
    conn.close()
    server_socket.close()
    print("Connessione chiusa")

# Funzione per inviare dati al server
def send_data(host="127.0.0.1", port=65432, message="Ciao dal client!"):
    time.sleep(2)  # Aspetta 2 secondi per far partire il server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connesso al server, invio dati...")
        client_socket.sendall(message.encode("utf-8"))
        print("Dati inviati!")

if __name__ == "__main__":
    # Avvia il server in un thread separato, con daemon=True
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Esegue un'azione che poi invia i dati
    print("Eseguendo altre operazioni...")
    send_data(message="Questo è un messaggio di test!")
    
    # Il programma principale attende un po' per permettere al server di ricevere e processare i dati
    time.sleep(5)
    print("Programma principale terminato.")
