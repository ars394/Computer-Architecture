# SPRINT CHALLENGE MVP: 
#  Add the CMP instruction and equal flag to your LS-8.
#  Add the JMP instruction.
#  Add the JEQ and JNE instructions.

### CMP

# *This is an instruction handled by the ALU.*

# `CMP registerA registerB`

# Compare the values in two registers.

# * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.

# * If registerA is less than registerB, set the Less-than `L` flag to 1,
#   otherwise set it to 0.

# * If registerA is greater than registerB, set the Greater-than `G` flag
#   to 1, otherwise set it to 0.

# Machine code:
# ```
# 10100111 00000aaa 00000bbb
# A7 0a 0b
# ```

### JMP

# `JMP register`

# Jump to the address stored in the given register.

# Set the `PC` to the address stored in the given register.

# Machine code:
# ```
# 01010100 00000rrr
# 54 0r
# ```

### JNE

# `JNE register`

# If `E` flag is clear (false, 0), jump to the address stored in the given
# register.

# Machine code:
# ```
# 01010110 00000rrr
# 56 0r
# ```

### JEQ

# `JEQ register`

# If `equal` flag is set (true), jump to the address stored in the given register.

# Machine code:
# ```
# 01010101 00000rrr
# 55 0r
# ```


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
        self.CALL = 0b0000
        self.RET = 0b0001
        

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
#CMP
        elif op == 'CMP':
            
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b100
            else:
                self.fl = 0b001
            

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        HLT = False

        while not HLT:
            
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            address_controller = ((IR & 0b11000000) >> 6) + 1
            instruction = IR & 0b00001111
            ALU = ((IR & 0b00100000) >> 5) 
            PC = ((IR & 0b00010000) >> 4) 
            #LDI
            if ALU == 1:
                if instruction in self.ALU_bt:
                    self.alu(self.ALU_bt[instruction], operand_a, operand_b)
                    self.pc += address_controller
                else:
                    raise Exception(f"{IR}Unsupported ALU operation")
            elif PC == 1:
                if instruction == self.CALL:
                    
                    pointer = self.pc + address_controller
                    
                    self.SP -= 1
                    self.ram_write(self.SP, pointer)
                    self.pc = self.reg[operand_a]
                
                elif instruction == self.RET:
                    pointer = self.ram_read(self.SP)
                    
                    self.SP += 1
                    self.pc = pointer    
# JMP  
                elif instruction == self.JMP:
                    self.pc = self.reg[operand_a]
# JEQ
                elif instruction == self.JEQ:
                    e_flag = self.fl & 0b00000001
                    
                    if e_flag == 1:
                        self.pc = self.reg[operand_a]
                    else:
                        self.pc += address_controller
# JNE 
                elif instruction == self.JNE:
                    e_flag = self.fl & 0b00000001
                    
                    if e_flag == 0:
                        self.pc = self.reg[operand_a]
                    else:
                        self.pc += address_controller

                else:
                    raise Exception(f"{IR}CP operation is not supported")
            else:
                if instruction == self.LDI:
                    self.reg[operand_a] = operand_b 
                    self.pc += address_controller
                
                elif instruction == self.PRN:
                    print(int(self.reg[operand_a]))
                    self.pc += address_controller
                
                elif instruction == self.HLT:
                    HLT = True

                elif instruction == self.PUSH:
                    self.SP -= 1
                    self.ram_write(self.reg[self.SP], operand_a)
                    self.pc += address_controller  

                elif instruction == self.POP:
                    byte = self.ram_read(self.reg[self.SP])
                    self.reg[operand_a] = byte
                    self.SP += 1
                    self.pc += address_controller

                else:
                    
                    raise Exception(f"Unsupported operation: {bin(IR)} at {self.pc}")
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value