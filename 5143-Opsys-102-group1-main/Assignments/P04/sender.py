from comms import Sender
import sys
import json
from rich import print
from generate_assembly import GenerateAssembly
import string
import itertools

#Poka, SlipperyDragon149!!!

# rabbitmq_host = "164.90.134.137"  # change as needed
# rabbitmq_user = "user1"  # change to your admin username
# rabbitmq_pass = "123456789"  # change to your admin password
# rabbitmq_port = 5672
# rabbitmq_exch = "cpuproject"

rabbitmq_host = "164.90.134.137"  # change as needed
rabbitmq_user = "Ellerkamp"  # change to your admin username
rabbitmq_pass = "SlipperyKoala371!!!"  # change to your admin password
rabbitmq_port = 5672
rabbitmq_exch = "cpuproject"

combinations = []
def get_key():
    chars = ""
    all_characters = list(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
    for i in all_characters:
        chars += i
    for i in range(6):
        combinations = ["".join(p) for p in itertools.product(str(chars), repeat=i)]
    file_path = "output.txt"

    # Write the combinations to the file
    with open(file_path, 'w') as file:
        for item in combinations:
            file.write(item + '\n')

if __name__ == "__main__":
#    combinations = get_key()
    with open("commsConfig.json") as f:
        config = json.load(f)

     # if len(sys.argv) < 5:
     #     print("Usage: sender.py <host> <port> <exchange> <routing_key> <message>")
     # else:
     #     print(sys.argv)
     #     host, port, exchange, routing_key, message, num = sys.argv[1:7]


#---------------------------------------------------------------------------------------
    # taylor swift prank code.
    # file_path = "output.txt"

    # sender = Sender(**config)
    # print(config)
        
    # lyrics = ""
    # with open(file_path, 'r') as file:
    #     for line in file:
    #         sender.send_message(message=lyrics,routing_key=str(line.strip()),host=rabbitmq_host,port=rabbitmq_port,exchange=rabbitmq_exch)


#-----------------------------------------------------------------------------------
    sender = Sender(**config)
    print(config)
        
    hex = []
    for i in range(10):
        hex.append(GenerateAssembly())
        
    sender.send_message(message=json.dumps(hex),routing_key="apples3",host=rabbitmq_host,port=rabbitmq_port,exchange=rabbitmq_exch)
