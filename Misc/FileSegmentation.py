import os


def divide(string, parts):
    k, m = divmod(len(string), parts)
    return (string[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(parts))


size = (os.path.getsize("1.mp4"))
with open("1.mp4", "rb") as mp4:
    data = mp4.read(size)

print(len(data))

parts1 = divide(data, 4)
parts = []
for i in parts1:
    parts.append(i)
print((len(parts[0]))+len((parts[1]))+(len(parts[2]))+len((parts[3])))
print(len(parts[0]))
print(len(parts[1]))
print(len(parts[2]))
print(len(parts[3]))
print(len(parts[3]))
file = open("fileRecombined.mp4", "wb")
file.write(parts[0]+parts[1]+parts[2]+parts[3])

data = file.read()
def segmentation(data, num):
    segment = []
    k, m = divmod(data, num)
    start = 0
    end = k
    
    for i in range(0, num, k):

        segment[i]= data[start : end]
        start = k
        end = k+k
    for k in (m):
        segment[i]+=k
