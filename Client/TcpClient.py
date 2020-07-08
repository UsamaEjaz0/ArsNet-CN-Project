import socket, os
import threading
import time
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--metric_interval', help="", type=int, default=2)
parser.add_argument('-o', '--output_location', help="", default="Received.mp4")
parser.add_argument('-a', '--server_ip_address', help="", default=socket.gethostbyname(socket.gethostname()))
parser.add_argument('-p', '--list_of_ports', nargs='+', help="")
parser.add_argument('-r', '--resume', help="", default=0)
args = parser.parse_args()


port_list = args.list_of_ports
port_list = list(map(int, port_list))
i_flag = args.metric_interval
file_location = args.output_location
host = args.server_ip_address
resume = int(args.resume)

segments = []
failed_servers = []
alive_servers =list(range(len(port_list)))
total_segments = list(range(len(port_list)))
to_be_received = []


downloaded_bytes = [0] * len(port_list)
download_speed = [0] * len(port_list)
total_bytes = [0] * len(port_list)
segment_numbers = []


def get_file_size():
    pass


def divide(num, div):
    return [num // div + (1 if x < num % div else 0) for x in range(div)]


received_segments = []

file_size = 0


count = 0
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
    global host
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



        server.connect((host, port_num))

        file_size = int((server.recv(1024)).decode())

        total_bytes = divide(file_size, len(port_list))

        data = b''
        if segment_num is None:
            segment_num = server_num

        receive_segment_from_server(server, server_num, segment_num)
        start = time.time()
        segment_numbers.append(int(server.recv(1024).decode()))

        for _ in (range(20)):
            data += server.recv(file_size)
            downloaded_bytes[server_num] = len(data)
        end = time.time()

        download_speed[server_num] = len(data)*0.001/(end-start)


        if segment_num in received_segments:
            pass
        else:

            segments.append(data)
            received_segments.append(segment_num)






        to_be_received = [item for item in total_segments if item not in received_segments]
        return server_num
    except Exception as e:
        failed_servers.append(server_num)
        alive_servers = [item for item in total_segments if item not in failed_servers]

        if resume:
            connect_to_server((server_num + 1) % len(port_list),
                              port_list[(server_num + 1) % len(port_list)], segment_num)


thread = []


def receive_segment_from_server(server, server_num, segment_num=None):
    segment_num_in_bytes = (str(segment_num)).encode()
    server.send(segment_num_in_bytes)


def start():
    if not resume:
        for i in range(len(port_list)):
            thread.append(threading.Thread(target=connect_to_server, args=(i, port_list[i])))
            thread[i].start()
            time.sleep(0.01)


def show_status(downloaded_bytes, total_bytes, download_speed):
    for i in range(len(port_list)):
        print(f"Server {i}: {downloaded_bytes[i]}/{total_bytes[i]}, download speed: {download_speed[i]} kb/s ")
    print(f"Total: {sum(downloaded_bytes)}/{file_size}, download speed: {sum(download_speed)/len(download_speed)} kb/s")



start()

if not resume:
    for i in range(len(port_list)-1, -1, -1):
        thread[i].join()


def refresh():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_status(downloaded_bytes, total_bytes, download_speed)


remaining_bytes = 0
for i in failed_servers:
    remaining_bytes += total_bytes[i]
to_be_added_bytes = divide(remaining_bytes, len(alive_servers))

i = 0

correct = downloaded_bytes[0]
refresh()

gotten_remaining_segs = False
used_server = 0
server_used_for_resume = 0


def get_remaining_segments():
    global gotten_remaining_segs
    global alive_servers
    global to_be_received
    global used_server
    global server_used_for_resume
    if len(to_be_received) != 0:
        for seg_num in to_be_received:
            server_used_for_resume = connect_to_server(alive_servers[0], port_list[alive_servers[0]], seg_num)
            used_server = alive_servers[0]
        gotten_remaining_segs = True


get_remaining_segments()
if gotten_remaining_segs:
    if not resume:
        for j in to_be_added_bytes:
            if downloaded_bytes[alive_servers[i]] != 0:
                downloaded_bytes[alive_servers[i]] += to_be_added_bytes[i]
            else:
                to_be_added_bytes.append(to_be_added_bytes[i])
            i += 1
    if sum(downloaded_bytes) != file_size:
        downloaded_bytes[used_server] += file_size-sum(downloaded_bytes)


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


if not resume:

    dumpFile = open("Dump.txt", "wb")

    for s in segments:

        dumpFile.write(bytes(b'lol'))
        dumpFile.write(s)

    dumpFile.close()
    received_segs = open("Received_segments.txt", "w")
    received_segs.write(str(segment_numbers))
    received_segs.close()

if resume:

    dumpFile = open("Dump.txt", "rb")
    segments = dumpFile.read()
    segments = segments.split(b'lol')
    segments.pop(0)

    dumpFile.close()

    received_segs = open("Received_segments.txt", "r")
    seg_nums = received_segs.read()

    seg_nums = seg_nums.replace("[", "")
    seg_nums = seg_nums.replace("]", "")
    seg_nums = (seg_nums.split(","))
    seg_nums = list(map(int,seg_nums))

    to_be_received = [item for item in str(total_segments) if item not in str(seg_nums)]
    bas_yar = to_be_received

    segment_numbers += seg_nums
    received_segs.close()

    get_remaining_segments()
    downloaded_bytes[server_used_for_resume] = 0
    for o in bas_yar:
        downloaded_bytes[server_used_for_resume] += total_bytes[server_used_for_resume]

    quick_sort(segments, segment_numbers, 0, len(segment_numbers) - 1)


data = bytearray()
for segment in segments:

    data.extend(segment)

chunk_size = 1024

with open(file_location, "wb") as file:
    file.write(data)

while True:
    time.sleep(i_flag)
    refresh()
