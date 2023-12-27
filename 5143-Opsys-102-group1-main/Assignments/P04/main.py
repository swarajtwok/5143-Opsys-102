import requests
import json
import sys

class Register:
    _global_id = 0
    _registers = []

    def __init__(self):
        self.id = Register._global_id
        Register._global_id += 1
        Register._registers.append(self)

        self.in_use = False  # Indicates whether the register is currently in use
        self.value = None  # The value held by the register

    def set_value(self, value):
        self.value = value
        self.in_use = True

    def release(self):
        self.value = None
        self.in_use = False

    def __repr__(self):
        return f"Register(ID: {self.id}, In Use: {self.in_use}, Value: {self.value})"

    @classmethod
    def get_all_registers(cls):
        return cls._registers

    # # Example Usage
    # reg1 = Register()
    # reg1.set_value(100)

    # reg2 = Register()
    # reg2.set_value(200)

    # print(reg1)  # Output: Register(ID: 0, In Use: True, Value: 100)
    # print(reg2)  # Output: Register(ID: 1, In Use: True, Value: 200)

    # reg1.release()
    # print(reg1)  # Output: Register(ID: 0, In Use: False, Value: None)

    # # Optional: Get all registers
    # all_registers = Register.get_all_registers()
    # print(all_registers)

    def __str__(self):
        return f"ID: {self.id}, Value: {self.value}"


class Registers:
    def __init__(self, num_registers=10):
        self.num_registers = num_registers
        self.registers = [Register() for x in range(self.num_registers)]

    def __str__(self):
        s = ""
        for r in self.registers:
            s += str(r)
        return s

def load(register, value):
    register.set_value(value)
    return register
def sub(register, value):
    register.set_value(register.value - value)
    return register
def sub(register, register2):
    register.set_value(register.value - register2.value)
    return register
def add(register, value):
    register.set_value(register.value + value)
    return register
def add(register, register2):
    register.set_value(register.value + register2.value)
    return register
def mul(register, value):
    register.set_value(register.value * value)
    return register
def mul(register, register2):
    register.set_value(register.value * register2.value)
    return register
def div(register, value):
    register.set_value(register.value / value)
    return register
def div(register, register2):
    register.set_value(register.value / register2.value)
    return register
def asub(register, value):
    register.set_value(abs(register.value - value))
    return register
def store(register, register2, register3, register4, register5):
    return f"\"STORE\":[{register.value},{register2.value},{register3.value}], \"xy\": [{register4.value},{register5.value}]"

if __name__ == "__main__":
    #get our data from the api call
    api_Connect = 'http://sendmessage.live:8001/grayscale?num=100'

    # Make a GET request
    response = requests.get(api_Connect)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # The API response is usually in JSON format, you can access it using response.json()
        api_data = response.json()
#        print(api_data)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    #now to process our data
    Reg_List = Registers()
    #process each sequence in the json file, each sequence will consists of a series of commands and ends with a store command
    for sequence in api_data:
 #       print(sequence)
        #now we must process each command in the sequence
        for command in sequence:
            comms = command.split()
            #now we must process each command
            print(command)
            if comms[0] == "LOAD":
                    Reg_List.registers[int(comms[1][1:])].set_value(int(comms[2]))
            elif comms[0] == "SUB":
                if comms[2][0] == "R":
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value - Reg_List.registers[int(comms[2][1:])].value)
                else:
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value - int(comms[2]))
            elif comms[0] == "ADD":
                if comms[2][0] == "R":
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value + Reg_List.registers[int(comms[2][1:])].value)
                else:
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value + int(comms[2]))
            elif comms[0] == "MUL":
                if comms[2][0] == "R":
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value * Reg_List.registers[int(comms[2][1:])].value)
                else:
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value * int(comms[2]))
            elif comms[0] == "DIV":
                if comms[2][0] == "R":
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value / Reg_List.registers[int(comms[2][1:])].value)
                else:
                    Reg_List.registers[int(comms[1][1:])].set_value(Reg_List.registers[int(comms[1][1:])].value / int(comms[2]))
            elif comms[0] == "ASUB":
                if comms[2][0] == "R":
                    Reg_List.registers[int(comms[1][1:])].set_value(abs(Reg_List.registers[int(comms[1][1:])].value - Reg_List.registers[int(comms[2][1:])].value))
                else:
                    Reg_List.registers[int(comms[1][1:])].set_value(abs(Reg_List.registers[int(comms[1][1:])].value - int(comms[2])))
            elif comms[0] == "STORE":
                print(f"\"STORE\":[{Reg_List.registers[int(comms[1][2:3])]},{Reg_List.registers[int(comms[1][5:6])]},{Reg_List.registers[int(comms[1][8:9])]}], \"xy\":[{Reg_List.registers[int(comms[2][2:3])]},{Reg_List.registers[int(comms[2][5:6])]}]")
            else:
                print(f"ERROR, add the new command to the program: {comms[0]}")
#    print(Reg_List)
#        print(sequence)
    #now to store our data
    