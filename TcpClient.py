import socket, os, time
import threading
from tqdm import tqdm
import time
port_list = [5050, 5051, 5052, 5053, 5054, 5055]

size = (os.path.getsize("1.mp4"))
segments = []
failed_servers = []
alive_servers = []
total_segments = list(range(len(port_list)))
to_be_received = []
def get_file_size():
    pass

received_segments = []
def connect_to_server(server_num, port_num, segment_num= None):
    global received_segments
    global total_segments
    global failed_servers
    global alive_servers
    global to_be_received
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        server.connect((host, port_num))
        #start = time.time()

        #print("here")
        data = b''
        if segment_num == None:
            segment_num = server_num

        receive_segment_from_server(server, server_num, segment_num)

        for i in (range(10)):
            data += server.recv(size)
        #end = time.time()

        #print(size* 0.001/(end-start))
        #print(size)

        if segment_num in received_segments:
            print("Already received once")
        else:
            segments.append(data)
            print(f"Segment {segment_num} received successfully")

        received_segments.append(segment_num)
        print(len(data))




        to_be_received = [item for item in total_segments if item not in received_segments]
        print(f"to be received {to_be_received}")

    except Exception as e:

        print(f"Server number {server_num} encountered a problem")
        failed_servers.append(server_num)
        alive_servers = [item for item in total_segments if item not in failed_servers]
        print(f"failed_serves {failed_servers}")
        print(f"alive_servers {alive_servers}")







thread = []

def receive_segment_from_server( server, server_num, segment_num = None):


    segment_num_in_bytes = (str(segment_num)).encode()
    server.send(segment_num_in_bytes)
def start():

    for i in range(len(port_list)):
        thread.append(threading.Thread(target=connect_to_server, args=(i, port_list[i])))
        thread[i].start()
        time.sleep(0.2)


start()


for i in range(len(port_list) -1, -1, -1):
    thread[i].join()


def get_remaining_segments():
    global alive_servers
    global to_be_received
    if len(to_be_received)!=0:
        for seg_num in to_be_received:
            connect_to_server(alive_servers[0], port_list[alive_servers[0]], seg_num )

get_remaining_segments()
data = bytearray()
for segment in segments:
    data.extend(segment)

chunk_size = 1024
with open("total.mp4", "wb") as file:
    file.write(data)