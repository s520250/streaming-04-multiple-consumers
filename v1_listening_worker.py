"""
Sammie Bever - January 27, 2023 - Streaming Data - Module 04 Assignment

Used anaconda prompt to run this script. Used 3 terminals - 1 ran the producer script (v1_emitter_of_tasks.py) 
and the other two terminals ran the consumer/worker script (this script)

See readme file for screenshot of running the v1 scripts.

__________________________________
Listens for task messages on the queue.
This process runs continously. 

Make as many listening workers as you need 
(start this process in multiple terminals).

Approach
---------
Work Queues - one task producer / many workers sharing work.


Terminal Reminders
------------------

- Use Control c to close a terminal and end a process.

- Use the up arrow to get the last command executed.

"""

import pika
import sys
import os
import time


def listen_for_tasks():
    """ Continuously listen for task messages on a named queue."""
    
    # create a blocking connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    # use the connection to create a communication channel
    ch = connection.channel()

    # define a callback function to be called when a message is received
    def callback(ch, method, properties, body):
        """ Define behavior on getting a message."""

        # decode the binary message body to a string
        print(f" [x] Received {body.decode()}")
        # simulate work by sleeping for the number of dots in the message
        time.sleep(body.count(b"."))
        # when done with task, tell the user
        print(" [x] Done")
        # acknowledge the message was received and processed 
        # (now it can be deleted from the queue)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # use the channel to declare a durable queue
    # a durable queue will survive a RabbitMQ server restart
    # and help ensure messages are processed in order
    # messages will not be deleted until the consumer acknowledges    
    ch.queue_declare(queue="task_queue", durable=True)
    print(" [*] Ready for work. To exit press CTRL+C")

    # The QoS level controls the # of messages 
    # that can be in-flight (unacknowledged by the consumer) 
    # at any given time. 
    # Set the prefetch count to one to limit the number of messages 
    # being consumed and processed concurrently.
    # This helps prevent a worker from becoming overwhelmed 
    # and improve the overall system performance.
    # prefetch_count = Per consumer limit of unaknowledged messages      
    ch.basic_qos(prefetch_count=1) 
    
    # configure the channel to listen on a specific queue,  
    # use the callback function named callback,
    # and do not auto-acknowledge the message (let the callback handle it)
    ch.basic_consume(queue="task_queue", on_message_callback=callback)

    # start consuming messages via the communication channel
    ch.start_consuming()


if __name__ == "__main__":
    try:
        listen_for_tasks()

    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
