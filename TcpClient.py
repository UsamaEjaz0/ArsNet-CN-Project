import socket, os, time
import threading
from tqdm import tqdm
import time
port_list = [5050, 5051, 5052, 5053, 5054, 5055, 5056, 5057]

i_flag = 2
segments = []
failed_servers = []
alive_servers = []
total_segments = list(range(len(port_list)))
to_be_received = []
resume = True
downloaded_bytes = [0] * len(port_list)
download_speed = [0] * len(port_list)
total_bytes = [0] * len(port_list)
segment_numbers = []
test1 = time.time()


def get_file_size():
    pass

def divide(num, div):
    return [num // div + (1 if x < num % div else 0) for x in range(div)]


received_segments = []

file_size = 0
def connect_to_server(server_num, port_num, segment_num= None):
    global received_segments
    global total_segments
    global failed_servers
    global alive_servers
    global to_be_received
    global download_speed
    global segment_numbers
    global total_bytes
    global file_size
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        #print(host)

        server.connect((host, port_num))

        file_size = int((server.recv(1024)).decode())

        total_bytes = divide(file_size, len(port_list))

        data = b''
        if segment_num is None:
            segment_num = server_num

        receive_segment_from_server(server, server_num, segment_num)
        start = time.time()
        segment_numbers.append(int(server.recv(1024).decode()))
        #print(segment_numbers)

        for i in (range(10)):
            data += server.recv(file_size)
            downloaded_bytes[server_num] = len(data)
        end = time.time()

        download_speed[server_num] = len(data)*0.001/(end-start)
        #print(download_speed)
        #print(size)

        if segment_num in received_segments:
            pass
        else:
            segments.append(data)
            #print(f"Segment {segment_num} received successfully")
            received_segments.append(segment_num)

        #print(len(data))




        to_be_received = [item for item in total_segments if item not in received_segments]
        #print(f"to be received {to_be_received}")

    except Exception as e:
        print(e)
        #print(f"Server number {server_num} encountered a problem")
        failed_servers.append(server_num)
        alive_servers = [item for item in total_segments if item not in failed_servers]
        #print(f"failed_serves {failed_servers}")
        #print(f"alive_servers {alive_servers}")


thread = []


def receive_segment_from_server(server, server_num, segment_num=None):
    segment_num_in_bytes = (str(segment_num)).encode()
    server.send(segment_num_in_bytes)


def start():

    for i in range(len(port_list)):
        thread.append(threading.Thread(target=connect_to_server, args=(i, port_list[i])))
        thread[i].start()
        time.sleep(0.01)


def show_status(downloaded_bytes, total_bytes, download_speed):
    for i in range(len(port_list)):
        print(f"Server {i}: {downloaded_bytes[i]}/{total_bytes[i]}, download speed: {download_speed[i]} kb/s ")
    print(f"Total : {sum(downloaded_bytes)}/{file_size}, download speed: {sum(download_speed)/len(download_speed)} kb/s")


if resume:
    start()

for i in range(len(port_list) -1, -1, -1):
    thread[i].join()



def refresh():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_status(downloaded_bytes, total_bytes, download_speed)


remaining_bytes = 0
for i in failed_servers:
    remaining_bytes += total_bytes[i]
to_be_added_bytes = divide(remaining_bytes, len(alive_servers))



i = 0
for j in to_be_added_bytes:
    if downloaded_bytes[alive_servers[i]] != 0:
        downloaded_bytes[alive_servers[i]] += to_be_added_bytes[i]
    else:
        to_be_added_bytes.append(to_be_added_bytes[i])
    i += 1


refresh()


def get_remaining_segments():

    global alive_servers
    global to_be_received
    if len(to_be_received) != 0:
        for seg_num in to_be_received:
            connect_to_server(alive_servers[0], port_list[alive_servers[0]], seg_num)


get_remaining_segments()



def partition(arr2, arr, low, high):
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):

        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            arr2[i], arr2[j] = arr2[j], arr2[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    arr2[i + 1], arr2[high] = arr2[high], arr2[i + 1]

    return i + 1


def quick_sort(arr2, arr, low, high):
    if low < high:
        pi = partition(arr2, arr, low, high)
        quick_sort(arr2, arr, low, pi - 1)
        quick_sort(arr2, arr, pi + 1, high)


quick_sort(segments, segment_numbers, 0, len(segment_numbers)-1)

data = bytearray()
for segment in segments:
    data.extend(segment)

chunk_size = 1024
with open("total.mp4", "wb") as file:
    file.write(data)

test2 = time.time()
print(test2 - test1)


# while True:
#     time.sleep(i_flag)
#     refresh()
