import socket
import time
import numpy as np

#Muñoz González Daniel Aurelio
#Aplicación que simula el juego de busca minas con dos máquinas comunicándose entre sí con hilos y varios clientes

# Cambiamos la IP por la del dispositivo o la de la máquina virtual según queramos el que sea el servidor
#HOST = "192.168.1.93"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024
jugandoP = 0


print("Ingresa la IP destino")
HOST = input()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    #Establece la conexión con el servidor
    TCPClientSocket.connect((HOST, PORT))
    #Recibe e imprime el mensaje de bienvenida
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    if(info == "Lo siento, pero no hay espacio para usted en la partida"):
        exit()
    #Recibe e imprime el mensaje de bienvenida
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    
    if(info == "principiante" or info == "Principiante"):
        # Creando el tablero
        print("Creando tablero nivel principiante")
        tablero = np.zeros((9, 9))
        while True:
            print("Haga su tiro en formato de número de dos números (xy), donde x representa la fila mientras que y representa la columna (números 0-8)")
            mensaje = input()
            TCPClientSocket.sendall(bytes(mensaje, "UTF-8"))
            data = TCPClientSocket.recv(buffer_size)
            info = str(data)[2:(len(str(data)) - 1)]
            print(info)
            if (info == "Okey"):
                tablero[int(mensaje[0]), int(mensaje[1])] = 8
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
            
            if (info == "Mina"):
                print("Has perdido")
                tablero[int(mensaje[0]), int(mensaje[1])] = 1
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
                data = TCPClientSocket.recv(buffer_size)
                info = str(data)[2:(len(str(data)) - 1)]
                print("Estuvo conectado: ", info, " segundos.")
                TCPClientSocket.close()
                break
    #Procedimiento en caso de seleccionar avanzado
    if(info == "avanzado" or info == "Avanzado"):
        # Creando el tablero
        print("Creando tablero nivel avanzado")
        tablero = np.zeros((16, 16))
        while True:
            print("Haga su tiro en formato de dos números conformados por dos dígitos cada uno (xxyy), donde xx representa la fila mientras que yy representa la columna (números 0-15)")
            mensaje = input()
            TCPClientSocket.sendall(bytes(mensaje, "UTF-8"))
            data = TCPClientSocket.recv(buffer_size)
            info = str(data)[2:(len(str(data)) - 1)]
            print(info)
            
            if (info == "Okey"):
                tablero[int(mensaje[0:2]), int(mensaje[2:4])] = 8
                print("\n")
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
                    print("\n----------------------------------------------------------------------------------------------------------------\n")
                    for w in range(16):  
                        print(w, "|", "\t", end="")
                        for y in range(16):          
                            print(int(tablero[w][y]), "\t", end="")
                        print("\n")
            if (info == "Mina"):
                print("Has perdido")
                tablero[int(mensaje[0:2]), int(mensaje[2:4])] = 1
                print(tablero)
                data = TCPClientSocket.recv(buffer_size)
                info = str(data)[2:(len(str(data)) - 1)]
                print("Estuvo conectado: ", info, " segundos.")
                TCPClientSocket.close()
                break
                
            if not data:
                print("No hubo datos :(")
                exit()
