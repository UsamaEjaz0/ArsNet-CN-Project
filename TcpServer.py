import sys
import socket, os, time
import threading
import pickle

# Gandu Parameters
time_interval = 2
num_of_servers = 4
port_list = [5050, 5051, 5052, 5053, 5054, 5055, 5056, 5057, 5058]
port_list = [5050, 5051, 5052, 5053]
status = [True] * num_of_servers
server_threads = []


def create_server(status, server_num, port_num):
    global server_sockets
    server_sockets = []

    host = socket.gethostbyname(socket.gethostname())
    server_sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    addr = (host, port_num)

    server_sockets[server_num].bind(addr)
    server_sockets[server_num].listen()
    try:
        while status[server_num]:
            conn, addr = server_sockets[server_num].accept()
            #print(f"[Client connected] ... ")

            size = (os.path.getsize("1.mp4"))
            with open("1.mp4", "rb") as mp4:

                data = mp4.read(size)


                sent_length = 0
                s = (int(conn.recv(1024)))
                #print(s)
                segments_gen = divide(data, num_of_servers)
                segments = []
                for k in segments_gen:
                    segments.append(k)

                sub_segments_gen = divide(segments[s], 10)
                sub_segments = []
                for k in sub_segments_gen:
                    sub_segments.append(k)

                for i in range(10):
                    conn.send(sub_segments[i])



                time.sleep(0.5)
                #print(f"Segment {s} from Server with port {port_num}")
                conn.close()
    except Exception as e:
        #print(e)
        pass




def send_segment(conn, addr, num, server_num):
    pass

def start(status):

    for i in range(num_of_servers):
        server_thread = threading.Thread(target=create_server, args=(status, i, int(port_list[i])))
        server_thread.start()
        print(f"Server {i}: Port: {port_list[i]} Status: {status[i]}, To shutdwon server {i} Press E{i} ")

def start_specific_server(status, server_num):
    create_server(status, server_num,  port_list[server_num])

def change_status(string):
    clear_screen()
    print(string[1:2])
    status[int(string[1:2])] = False
    server_sockets[int(string[1:2])].close()
    for i in range(num_of_servers):
        print(f"Server {i}: Port: {port_list[i]} Status: {status[i]}, To shutdwon server {i} Press E{i} ")


start(status)


def divide(string, parts):
    k, m = divmod(len(string), parts)
    return (string[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(parts))


def clear_screen():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print('\n'*50)


while True:
    inp = input()
    change_status(inp)
    print(inp)


