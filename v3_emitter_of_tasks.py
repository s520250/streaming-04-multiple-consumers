"""
Sammie Bever - January 27, 2023 - Streaming Data - Module 04 Assignment

    This program sends a message to a queue from a csv file on the RabbitMQ server.
    Each CSV row is considered a task.
    Make tasks harder/longer-running by adding dots at the end of the message.

    See readme file for screenshot of running the v3 scripts.
    Ran 3 Anaconda prompt terminals - 1 emitter of tasks (producer) and 2 listening workers (consumers).
    Added option to show/not show the offer question to open RabbitMQ server.

    Author: Sammie Bever
    Date: January 27, 2023

"""
## copied  some code from v2 of this assignment (module 4)
## adding my own code to read from csv file 

import pika
import sys
import webbrowser
import csv
import socket
import time

# define option to open RabbitMQ admin webpage
def offer_rabbitmq_admin_site(show_offer):
    # including show_offer variable to give the option to turn off the offer to open RabbitMQ
    # Can tell it to be on or off later in the code
    if show_offer == True:
        """Offer to open the RabbitMQ Admin website"""
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

# define a message to send to queue
def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """
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

    # did not include reversed sort for chronological order like we did in mod 2
    # reversed = sorted(input_file)

    # create a csv reader for our comma delimited data
    # changed reversed option to input_file
    reader = csv.reader(input_file, delimiter=',')

    # read rows from csv (slowly)
    for row in reader:
        # read a row from the file
        input_file.read

        # use an fstring to create a message from our data
        # notice the f before the opening quote for our string?
        fstring_message = f"{row}"

        # prepare a binary (1s and 0s) message to stream
        # MESSAGE is case sensitive!!
        MESSAGE = fstring_message.encode()

        # use the socket sendto() method to send the message
        sock.sendto(MESSAGE, address_tuple)
        # print (f"Sent: {MESSAGE}.")

        # sleep for a few seconds
        time.sleep(5)

# when indented under the row for row code, it sends each row of the csv as a separate message/task,
# which is what we want it to do.
        try:
            # create a blocking connection to the RabbitMQ server
            conn = pika.BlockingConnection(pika.ConnectionParameters(host))
            # use the connection to create a communication channel
            ch = conn.channel()
            # use the channel to declare a durable queue
            # a durable queue will survive a RabbitMQ server restart
            # and help ensure messages are processed in order
            # messages will not be deleted until the consumer acknowledges
            ch.queue_declare(queue=queue_name, durable=True)
            # use the channel to publish a message to the queue
            # every message passes through an exchange
            ch.basic_publish(exchange="", routing_key=queue_name, body=MESSAGE)
            # print a message to the console for the user
            print(f" [x] Sent {MESSAGE}")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error: Connection to RabbitMQ server failed: {e}")
            sys.exit(1)
        finally:
            # close the connection to the server
            conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    # show_offer variable is set to False/off for RabbitMQ site
    show_offer = False
    offer_rabbitmq_admin_site(show_offer)
    # get the message from the command line
    # if no arguments are provided, use the default message
    # use the join method to convert the list of arguments into a string
    # join by the space character inside the quotes
    message = " ".join(sys.argv[1:])  or "{message}"
    # send the message to the queue
    send_message("localhost","task_queue3",message)

