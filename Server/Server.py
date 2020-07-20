import socket, os, time
import threading
import argparse

parser = argparse.ArgumentParser()

# adding parameters
parser.add_argument('-i', '--status_interval', help="", type=int, default=2)
parser.add_argument('-n', '--num_servers', help="", type=int)
parser.add_argument('-f', '--file_location', help="", default="to_be_sent.mp4")
parser.add_argument('-p', '--list_of_ports', nargs='+', help="", type=int)
args = parser.parse_args()


port_list = [5050, 5051, 5052, 5053, 5054, 5055, 5056, 5057]

i_flag = args.status_interval
num_of_servers = args.num_servers
file_location = args.file_location
port_list = args.list_of_ports

status = [True] * num_of_servers
server_threads = []

for i in port_list:
    if i >1023 and i < 65535:
        print("Enter valid port number")
        break
        exit()
def create_server(status, server_num, port_num):

    """Creates a new server

:param status: list of all the servers' status
:type status: bool list
:param server_num: Server Number which is being created
:type server_num: int
:param port_num: port number on which server is being created
:type port_num: int
"""

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

            size = (os.path.getsize(file_location))
            with open(file_location, "rb") as mp4:

                data = mp4.read(size)
                size = str(size).encode()
                conn.send(size)

                sent_length = 0
                s = (int(conn.recv(1024)))
                segments_gen = divide(data, num_of_servers)
                segments = []
                for k in segments_gen:
                    segments.append(k)

                sub_segments_gen = divide(segments[s], 20)
                sub_segments = []
                for k in sub_segments_gen:
                    sub_segments.append(k)
                seg_num = str(s).encode()
                conn.send(seg_num)
                for i in range(20):
                    conn.send(sub_segments[i])



                time.sleep(0.5)
                conn.close()
    except Exception as e:
        pass


def start(status):

    """Starts all the servers and threads

:param status: A list of current status of every server
:type status: bool list

"""

    for i in range(num_of_servers):
        server_thread = threading.Thread(target=create_server, args=(status, i, int(port_list[i])))
        server_thread.start()
        print(f"Server {i}: Port: {port_list[i]} Status: {status[i]}, To shutdwon server {i} Press E{i} ")


def start_specific_server(status, server_num):
    """Starts a specific server

:param status: A list of current status of every server
:type status: bool list
:param server_num: Server number which is to be started
:type server_num: int
"""
    create_server(status, server_num,  port_list[server_num])


def change_status(string):
    """changes the status of a particular server

:param string: String containing the server number to close
:type string: str
"""
    clear_screen()
    print(string[1:2])
    status[int(string[1:2])] = False
    server_sockets[int(string[1:2])].close()
    for i in range(num_of_servers):
        print(f"Server {i}: Port: {port_list[i]} Status: {status[i]}, To shutdwon server {i} Press E{i} ")


start(status)


def divide(string, parts):

    """Divides the input string of bytes into "parts" parts.

:param string: The byte string to be divided
:type string: byte
:param parts: Number of parts in which the string is to be divided
:type parts: int
:returns: a list of bytes
:rtype: list
"""
    k, m = divmod(len(string), parts)
    return (string[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(parts))


def refresh():

    """Refreshes the status of server

"""
    while True:
        time.sleep(i_flag)
        clear_screen()
        for i in range(num_of_servers):
            print(f"Server {i}: Port: {port_list[i]} Status: {status[i]}, To shutdwon server {i} Press E{i} ")


def clear_screen():

    """Clear Console Screen

"""
    os.system('cls' if os.name == 'nt' else 'clear')


outputThread = threading.Thread(target=refresh)
outputThread.start()
while True:
    inp = input()
    change_status(inp)
    print(inp)
