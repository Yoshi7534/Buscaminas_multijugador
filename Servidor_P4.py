import socket
import time
import threading
import numpy as np

# Muñoz González Daniel Aurelio
# Aplicación que simula el juego de busca minas con dos máquinas comunicándose entre sí con hilos y varios clientes

# HOST = "172.100.85.114"
HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
# Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
PORT = 65432
buffer_size = 1024


def servirPorSiempre(socketTcp, listaConexiones, tablero, dificultad, TCPServerSocket):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaConexiones.append(client_conn)
            gestion_conexiones(listaConexiones)
            time.sleep(2)
            thread_read = threading.Thread(target=juego, args=[client_conn, client_addr, tablero, dificultad])
            thread_read.start()
    except Exception as e:
        print(e)


def gestion_conexiones(listaConexiones):
    for conn in listaConexiones:
        if conn.fileno() == -1:
            listaConexiones.remove(conn)
    print("\nHilos activos:", threading.active_count())
    print("\nEnumerar", threading.enumerate())
    print("\nTamaño y lista de conexiones: ", len(listaConexiones))
    print(listaConexiones)


def juego(Client_conn, Client_addr, tablero, dificultad):
    try:
        print("Estamos jugando en ", dificultad, "\n")
        # La siguiente línea podría utilizarse para obtener info más específica sobre el hilo específico de cada cliente
        cur_thread = threading.current_thread()
        print("\nConectado a", Client_addr)
        inicio = time.time()
        print("Nuevo cliente detectado")
        # Mensaje de bienvenida
        Client_conn.sendall(b"Vamos a jugar buscaminas en dificultad: ")
        Client_conn.sendall(bytes(dificultad, "UTF-8"))
        time.sleep(3)
        while True:
            print("Esperando el siguiente tiro: ")
            data = Client_conn.recv(buffer_size)
            print(cur_thread)
            info = str(data)[2:(len(str(data)) - 1)]
            print(info)
            if not data:
                print("No hubo datos :(")
            if (tablero[int(info[0]), int(info[1])]):
                Client_conn.sendall(b"Mina")
                print("El cliente pisó una mina")
                fin = time.time()
                despedida = "Estuvo conectado " + \
                    str(fin-inicio) + " segundos."
                print(despedida)
                Client_conn.sendall(bytes(str(fin-inicio),  "UTF-8"))
                break
            else:
                tablero[int(info[0]), int(info[1])] = "8"
                # print(tablero)
                if (tablero.size == 81):
                    print(" ", "\t", end="")
                    for z in range(9):
                        print(z, "\t", end="")
                    print("\n---------------------------------------------------------------------\n")
                    for w in range(9):
                        print(w, "|", "\t", end="")
                        for y in range(9):
                            print(int(tablero[w][y]), "\t", end="")
                        print("\n")
                else:
                    print(" ", "\t", end="")
                    for z in range(16):
                        print(z, "\t", end="")
                    print("\n---------------------------------------------------------------------\n")
                    for w in range(16):
                        print(w, "|", "\t", end="")
                        for y in range(16):
                            print(int(tablero[w][y]), "\t", end="")
                        print("\n")
                Client_conn.sendall(b"Okey")
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()


def Iniciar(dificultad):
    if (dificultad == "principiante" or dificultad == "Principiante"):
        # Creamos el tablero para principiantes
        print("Vamos a jugar principiante")

        # Creando el tablero
        print("Creando tablero nivel principiante...")
        tablero = np.zeros((9, 9))
        minas = np.zeros(9)
        for k in range(10):
            fila = np.random.randint(0, 9)
            col = np.random.randint(0, 9)
            tablero[fila, col] = 1
            minas[col] = fila
            print("Mina colocada en: ", fila, col)

    elif(dificultad == "avanzado" or dificultad == "Avanzado"):
        #Creamos el tablero para avanzados  
        print("Vamos a jugar avanzado")

        # Creando el tablero
        print("Creando tablero nivel avanzado...")
        tablero = np.zeros((16, 16))
        minas = np.zeros(40)
        for k in range(40):
            fila = np.random.randint(0, 15)
            col = np.random.randint(0, 15)
            tablero[fila, col] = 1
            minas[col] = fila
            print("Mina colocada en: ", fila, col)

    else:
        print("Ingrese una dificultad válida, por favor")
        dificultad = input("Puede ser principiante (9x9) o avanzado (40x40)\n")
        tablero = Iniciar(dificultad)
    
    return tablero    

listaConexiones = []
numConn = input("Ingresa el numero de jugadores simultaneos:\n")
dificultad = input("Ingrese su dficultad, puede ser principiante (9x9) o avanzado (40x40)\n")
tablero = Iniciar(dificultad)

# Semáforo para controlar la conexión de los jugadores
player_semaphore = threading.Semaphore(int(numConn))

# Función para aceptar conexiones de los jugadores
def accept_connections(socketTcp, listaConexiones, tablero, dificultad):
    while True:
        client_conn, client_addr = socketTcp.accept()
        print("Conectado a", client_addr)
        if player_semaphore.acquire(blocking=False):
            listaConexiones.append(client_conn)
            gestion_conexiones(listaConexiones)
            time.sleep(2)
            # Esperar a que se conecten todos los jugadores
            while len(listaConexiones) < (int(numConn)):
                print(len(listaConexiones))
                print(int(numConn))
                time.sleep(1)  
            
            thread_read = threading.Thread(target=juego, args=[client_conn, client_addr, tablero, dificultad])
            thread_read.start()
            client_conn.sendall(b"Jugador aceptado en la partida")
        else:
            client_conn.sendall(b"Lo siento, pero no hay espacio para usted en la partida")
            client_conn.close()

if (tablero.size == 81):
    print(" ", "\t", end="")
    for z in range(9):
        print(z, "\t", end="")
    print("\n---------------------------------------------------------------------\n")
    for w in range(9):
        print(w, "|", "\t", end="")
        for y in range(9):
            print(int(tablero[w][y]), "\t", end="")
        print("\n")
else:
    print(" ","\t",end="")
    for z in range(16):
        print(z,"\t",end="")
    print("\n---------------------------------------------------------------------\n")
    for w in range(16):  
        print(w, "|", "\t", end="")
        for y in range(16):          
            print(int(tablero[w][y]), "\t", end="")
        print("\n")
        

            
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    
    accept_thread = threading.Thread(target=accept_connections, args=[TCPServerSocket, listaConexiones, tablero, dificultad])
    # Iniciar hilo para aceptar conexiones
    accept_thread.start()

    # Esperar a que se conecten todos los jugadores
    #accept_thread.join()
    
        
    servirPorSiempre(TCPServerSocket, listaConexiones, tablero, dificultad, TCPServerSocket)