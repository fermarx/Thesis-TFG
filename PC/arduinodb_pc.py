from azure.servicebus import ServiceBusClient, ServiceBusMessage
from database import *
import time, datetime


while True:  
    # Connection string and namespace
    servicebus_client = ServiceBusClient.from_connection_string("Endpoint=sb://servicebus-tfg2022.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=key")
  
    global currentTinF, currentTinC,text_currentT
    currentTinF, currentTinC, text_currentT = arduino_read_T(arduino, 1)

    sender = servicebus_client.get_queue_sender(queue_name="myqueue")
    # Create a Service Bus message and send it to the queue
    message = ServiceBusMessage(str(currentTinF))
    sender.send_messages(message)
    print(f"{datetime.datetime.now()} -> Local sent: {currentTinF}")

    time.sleep(10)
    
    receiver = servicebus_client.get_queue_receiver(queue_name="myqueue2")
    received_msgs = receiver.receive_messages(max_wait_time=15, max_message_count=20)
    for msg in received_msgs:
        print(f"{datetime.datetime.now()} -> Local received: " + str(msg))
        if str(msg) == "cold": arduino.write(bytes("cold", 'utf-8'))
        elif str(msg) == "hot": arduino.write(bytes("hot", 'utf-8'))
        # complete the message so that the message is removed from the queue
        receiver.complete_message(msg)
    servicebus_client.close()