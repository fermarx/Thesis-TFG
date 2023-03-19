from azure.servicebus import ServiceBusClient, ServiceBusMessage
import pyodbc
import time, datetime

def init_db():
    server = 'mysqlserver-tfg2022.database.windows.net'
    database = 'plants'
    username = 'azureuser'
    password = 'pwd'    
    driver= '{ODBC Driver 17 for SQL Server}'
    conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn.cursor()


cursor = init_db()

while True:
    # Connection string and namespace
    servicebus_client = ServiceBusClient.from_connection_string("Endpoint=sb://servicebus-tfg2022.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=key")

    receiver = servicebus_client.get_queue_receiver(queue_name="myqueue")
    received_msgs = receiver.receive_messages(max_wait_time=15, max_message_count=20)
    for msg in received_msgs:
        print(f"{datetime.datetime.now()} -> Cloud received: " + str(msg))
        # Create a cursor object to execute SQL commands:
        cursor.execute("SELECT * FROM my_plants")
        rows = cursor.fetchall()
        list_cold = []
        list_hot = []
        for row in rows:
            if (float(str(msg)) < row[24]): list_cold.append(row)
            elif (float(str(msg)) > row[25]): list_hot.append(row)
            row = cursor.fetchone() # Move to the next row
        if list_cold and list_hot: message = "hot_cold"
        elif list_cold: message = "cold"
        elif list_hot: message = "hot"
        else: message = "ok"
        # complete the message so that the message is removed from the queue
        receiver.complete_message(msg)

        sender = servicebus_client.get_queue_sender(queue_name="myqueue2")
        # Create a Service Bus message and send it to the queue
        back = ServiceBusMessage(message)
        sender.send_messages(back)
        print(f"{datetime.datetime.now()} -> Cloud sent: {message}")
    
    servicebus_client.close()
    time.sleep(10)
