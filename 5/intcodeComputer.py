#!/usr/bin/python3
import sys

class IntcodeComputer:
    #left-pads a list with leading zeroes until specified length
    def padModes(self, modes, length):
        return (length * [0] + modes)[-length:]

    def readArgument(self, mode, argument):
        try:
            if (mode == 1):
                return argument
            else:
                return self.code[argument]
        except IndexError:
            return self.code[argument]

    def readOp(self):
        opcode = [int(x) for x in str(self.code[self.pc])]
        try:
            opcode[-2] = 10 * opcode[-2] + opcode[-1]
            del opcode[-1]
        except IndexError:
            pass #single-digit opcode will IndexError; this is expected
        try:
            self.ops[opcode[-1]](opcode[:-1]) #calls opcode[-1], with all previous elements as arguments OR empty list
            # opcode 1 will thus pass as self.opAdd([]), while opcode 1001 will pass as self.opAdd([1,0])
        except KeyError:
            print("No opcode %d found" % self.code[self.pc])
            sys.exit()

    def opAdd(self, modes):
        modes = self.padModes(modes, 3)
        x = int(self.readArgument(modes[-1], self.code[self.pc+1])) 
        y = int(self.readArgument(modes[-2], self.code[self.pc+2]))
        self.code[self.code[self.pc+3]] = x + y
        self.pc += 4

    def opMult(self, modes):
        modes = self.padModes(modes, 3)
        x = int(self.readArgument(modes[-1], self.code[self.pc+1]))
        y = int(self.readArgument(modes[-2], self.code[self.pc+2]))
        self.code[self.code[self.pc+3]] = x * y
        self.pc += 4

    def opMov(self, modes):
        self.code[self.code[self.pc+1]] = input("Awaiting input... ")
        self.pc += 2

    def opPrint(self, modes):
        print(self.code[self.code[self.pc+1]])
        self.pc += 2

    def opExit(self, modes):
        sys.exit()

    def run(self):
        while (self.pc < len(self.code)):
            self.readOp()

    def __init__(self, code):
        self.code = [int(i) for i in code] #translates everything to int
        self.pc = 0
        self.ops = {
                 1 : self.opAdd,
                 2 : self.opMult,
                 3 : self.opMov,
                 4 : self.opPrint,
                99 : self.opExit
                }

if __name__ == "__main__":
    print("this is a module; import it")