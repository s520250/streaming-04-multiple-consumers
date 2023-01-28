import csv
import socket
import time

host = "localhost"
port = 9999
address_tuple = (host, port)

# use an enumerated type to set the address family to (IPV4) for internet
socket_family = socket.AF_INET 

# use an enumerated type to set the socket type to UDP (datagram)
socket_type = socket.SOCK_DGRAM 

# use the socket constructor to create a socket object we'll call sock
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# read from a file to get some fake data
input_file = open("tasks.csv", "r")
output_file = open("v3_out.txt", "w")

# create a csv reader for our comma delimited data
reader = csv.reader(input_file, delimiter=',')

for row in reader:
    # read a row from the file
    values = row

    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
    fstring_message = f"{values}"

    # prepare a binary (1s and 0s) message to stream
    MESSAGE = fstring_message.encode()

    # use the socket sendto() method to send the message
    sock.sendto(MESSAGE, address_tuple)
    print (f"Sent: {MESSAGE}.")

    # send results to out10.txt file
    output_file.write(f"Sent: {MESSAGE}\n")

    # sleep for a few seconds
    time.sleep(3)