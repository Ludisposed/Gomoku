import socket
target_host = "0.0.0.0"
target_port = 9999

# Create
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect
client.connect((target_host,target_port))
# Send
sendstring = raw_input("What do we want to send>>> ")
client.send(sendstring)
# Recieve
response = client.recv(4096)

print response 
