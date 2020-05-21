# """CPU functionality."""

# import sys

# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         self.ram = [0] * 256
#         self.reg = [0] * 8
#         self.pc = self.reg[0]
#         self.commands = {
#             0b00000001: self.hlt,
#             0b10000010: self.ldi,
#             0b01000111: self.prn
#         }

#     def ram_read(self, address):
#         return self.ram[address]

#     def ram_write(self, value, address):
#         self.ram[address] = value

#     def hlt(self, operand_a, operand_b):
#         return (0, False)

#     def ldi(self, operand_a, operand_b):
#         self.reg[operand_a] = operand_b
#         return (3, True)

#     def prn(self, operand_a, operand_b):
#         print(self.reg[operand_a])
#         return (2, True)

#     def run(self):
#         address = 0

#         running = True

#         while running:
#             ir = self.ram[self.pc]

#             operand_a = self.ram_read(self.pc + 1)
#             operand_b = self.ram_read(self.pc + 2)

#             try:
#                 operation_output = self.commands[ir](operand_a, operand_b)
#                 running = operation_output[1]
#                 self.pc += operation_output[0]

#             except:
#                 print(f"command: {ir}")
#                 sys.exit()
        
#         # HLT = False

#         # while not HLT:
#         #     IR = self.ram_read(address) #instruction register
#         #     operand_a = self.ram_read(address + 1)
#         #     operand_b = self.ram_read(address + 2)
#         #     #LDI
#         #     if IR == self.LDI:
#         #         self.reg[operand_a] = operand_b
#         #         address += 3
#         #     #PRN
#         #     elif IR == self.PRN:
#         #         print(int(self.reg[operand_a]))
#         #         address += 2
#         #     #HLT
#         #     elif IR == self.HLT:
#         #         HLT = True

#     # def load(self, location):
#     #     """Load a program into memory."""

#     #     address = 0

#     #     # For now, we've just hardcoded a program:
#     #     code = open(location, 'r')
#     #     lines = code.readlines()
#     #     program = []

#     #     for line in lines:
#     #         if line[0] == '1' or line[0] == '0':
#     #             program.append(int(line[:8], 2))
#     #     for instruction in program:
#     #         self.ram[address] = instruction
#     #         address += 1


#     def load(self):
#             """Load a program into memory."""

#             address = 0

#             # For now, we've just hardcoded a program:

#             program = [
#                 # From print8.ls8
#                 0b10000010, # LDI R0,8
#                 0b00000000,
#                 0b00001000,
#                 0b01000111, # PRN R0
#                 0b00000000,
#                 0b00000001, # HLT
#             ]

#             for instruction in program:
#                 self.ram[address] = instruction
#                 address += 1

#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         #elif op == "SUB": etc
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             #self.fl,
#             #self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0]*8
        self.ram = [0]*256
        self.pc = 0
        self.fl = 0b0
        self.SP = 7
        self.reg[self.SP] = 0xF4
        #Primary Ops
        self.HLT = 0b1
        self.LDI = 0b0010
        self.PRN = 0b0111
        self.PUSH = 0b0101
        self.POP = 0b0110
        self.PUSH = 0b0101
        self.POP = 0b0110

        #ALU Ops
        self.ALU_bt = {
            0b0010: "MUL",  
            0b0000: 'ADD',  
            0b0001: 'SUB',  
            0b0011: 'DIV',  
            0b0100: 'MOD',  
            0b0101: 'INC',  
            0b0110: 'DEC',  
            0b0111: 'CMP',  
            0b1000: 'AND',  
            0b1001: 'NOT',  
            0b1010: 'OR' , 
            0b1011: 'XOR',  
            0b1100: 'SHL',  
            0b1101: 'SHR',
            0b1111: 'TST'   
        }
        
        #CP Ops
        self.JMP = 0b0100
        self.JNE = 0b0110
        self.JEQ = 0b0101
        

    def load(self, location):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        code = open(location, 'r')
        lines = code.readlines()
        program = []

        for line in lines:
            if line[0] == '1' or line[0] == '0':
                program.append(int(line[:8], 2))
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV':
            self.reg[reg_a] = self.reg[reg_a] / self.reg[reg_b]
        elif op == 'MOD':
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == 'INC':
            self.reg[reg_a] += 1
        elif op == 'DEC':
            self.reg[reg_a] -= 1
        elif op == 'AND':
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]  
        elif op == 'OR':
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == 'SHL':
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] > self.reg[reg_a]:
                self.fl = 0b010
            elif self.reg[reg_a] < self.reg[reg_a]:
                self.fl = 0b100
            else:
                self.fl = 0b001
        elif op == "TST":
            if self.reg[reg_a] == self.reg[reg_b]:
                print(f'Passed: {self.reg[reg_a]} == {self.reg[reg_b]}')
            else:
                print(f'Failed: {self.reg[reg_a]} != {self.reg[reg_b]}')
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        address = 0
        
        HLT = False

        while not HLT:
            self.pc = address
            IR = self.ram_read(address)
            operand_a = self.ram_read(address + 1)
            operand_b = self.ram_read(address + 2)
            address_controller = ((IR & 0b11000000) >> 6) + 1
            instruction = IR & 0b00001111
            ALU = ((IR & 0b00100000) >> 5) 
            CP = ((IR & 0b00010000) >> 4) 
            #LDI
            if ALU == 1:
                if instruction in self.ALU_bt:
                    self.alu(self.ALU_bt[instruction], operand_a, operand_b)
                    address += address_controller
                else:
                    raise Exception("Unsupported ALU operation")
            elif CP == 1:
                raise Exception("Unsupported CP operation")
            else:
                if instruction == self.LDI:
                    self.reg[operand_a] = operand_b 
                    address += address_controller
                
                elif instruction == self.PRN:
                    print(int(self.reg[operand_a]))
                    address += address_controller
                
                elif instruction == self.HLT:
                    HLT = True

                # elif instruction == self.PUSH:
                #     self.SP -= 1
                #     self.ram_write(self.reg[self.SP], operand_a)
                #     address += address_controller  

                # elif instruction == self.POP:
                #     byte = self.ram_read(self.reg[self.SP])
                #     self.reg[operand_a] = byte
                #     self.SP += 1
                #     address += address_controller

                else:
                    raise Exception("Unsupported operation")
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value
    
