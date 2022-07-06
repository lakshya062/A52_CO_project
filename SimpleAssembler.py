import sys

# dict1
opcode = {"add": "10000", "sub": "10001", "mov_imm": "10010", "mov_reg": "10011", "ld": "10100", "st": "10101", "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor":"11010", "or": "11011", "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111", "hlt": "01010"}

# dict2
type = {"add": "A", "sub": "A", "mov_imm": "B", "mov_reg": "C", "ld": "D", "st": "D", "mul": "A", "div": "C", "rs": "B", "ls": "B", "xor": "A", "or": "A", "and": "A", "not": "C", "cmp": "C", "jmp": "E", "jlt": "E", "jgt": "E", "je": "E", "hlt": "F"}

# dict3
flags = {"V": "00000000000000001000 ", "L": "00000000000000000100 ", "G": "00000000000000000010 ", "E": "00000000000000000001 "}

# dict4
reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

# dict5
reg_val = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0}

# dict6
var = {}

# dict7
labels = {}

# dict8
var_addr = {}

count_addr = -1
count_var = 0
hlt_count = 0
FLAG = 0
count_lab = 0

instructions = []

def calc_A(l1):
    global reg_val, flags, FLAG
    num = 0
    if l1[0] == "add":
        num = reg_val[l1[2]] + reg_val[l1[3]]
    if l1[0] == "mul":
        num = reg_val[l1[2]] * reg_val[l1[3]]
    if l1[0] == "sub":
        num = reg_val[l1[2]] - reg_val[l1[3]]
    if l1[0] == "xor":
        num = reg_val[l1[2]] ^ reg_val[l1[3]]
    if l1[0] == "or":
        num = reg_val[l1[2]] | reg_val[l1[3]]
    if l1[0] == "and":
        num = reg_val[l1[2]] & reg_val[l1[3]]
    if num >= 0 & num <= 255:
        reg_val[l1[0]] = num
        print_A(l1)
    elif num < 0 and num > 255:
        print("Error: Illegal Immediate values (less than 0 or more than 255)")
        sys.exit()
    else:
        reg_val[l1[1]] = 0
        FLAG = flags["v"]
        print(FLAG)


def calc_cmp(l1):
    global reg_val, FLAG, flags
    if reg_val[l1[1]] <= reg_val[l1[2]]:
        FLAG = "0000000000000010"
    elif reg_val[l1[1]] < reg_val[l1[2]]:
        FLAG = "0000000000000100"
    else:
        FLAG = "0000000000000001"


def print_A(l1):
    print(opcode[l1[0]] + "0" * 2 + reg[l1[1]] + reg[l1[2]] + reg[l1[3]])


def print_B(l1, t):
    print(opcode[l1[0]] + reg[l1[1]] + "0" * t, end='')


def print_B_mov(l1, t):
    print(opcode["mov_imm"] + reg[l1[1]] + "0" * t, end='')


def print_C_mov(l1):
    print(opcode["mov_reg"] + "0" * 5 + reg[l1[1]] + reg[l1[2]])


def DeciToBin(num):
    return bin(num).replace("0b", "")


def BinToDeci(n):
    return int(n, 2)


def print_C(l1):
    print(opcode[l1[0]] + "0" * 5 + reg[l1[1]] + reg[l1[2]])


def print_D(l1, t):
    print(opcode[l1[0]] + reg[l1[1]] + "0" * t, end='')


def print_E(l1, t):
    print(opcode[l1[0]] + "0" * 3 + "0" * t, end='')


def print_F(l1):
    print(opcode[l1[0]] + "0" * 11)


# MAIN
if __name__ == '__main__':
    while True:
        try:
            line = input().strip()
            if line == '':
                continue
            l1 = line.split()
            instructions.append(l1)
        except:
            break


        if ":" in l1[0]:
            labels[l1[0][:-1]] = count_lab
            l1.pop(0)
        count_lab += 1

    for i in range(0, len(instructions)):
        l1 = instructions[i]

        if l1[0] not in opcode and l1[0] != "var" and ":" not in l1[0] and l1[0] != "mov":
            print("Error: Typos in instruction name")
            sys.exit()

        if instructions[0] == 'hlt' and i != len(instructions) - 1:
            print('Error: ')

        if l1[0] == "var":
            if count_addr == -1:
                var.update({l1[0]: 0})
                var[l1[1]] = i

                count_var = count_var + 1
            else:
                print("Error : Variable not defined at the beginning")
                sys.exit()
        else:
            count_addr = count_addr + 1

            # Type A
            if l1[0] == "add" or l1[0] == "sub" or l1[0] == "mul" or l1[0] == "xor" or l1[0] == "or" or \
                    l1[0] == "and":
                if len(l1) != 4:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                elif l1[1] == 'FLAGS' or l1[2] == 'FLAGS' or l1[3] == 'FLAGS':
                    print("Error: Illegal use of FLAGS register")
                    sys.exit()
                elif l1[1] not in reg and l1[2] not in reg and l1[3] not in reg:
                    print("Error: Typos in register name")
                    sys.exit()
                else:
                    calc_A(l1)

            # Type B
            if l1[0] == "rs" or l1[0] == "ls":
                if len(l1) != 3:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                elif l1[1] == 'FLAGS' or l1[2] == 'FLAGS':
                    print("Error: Illegal use of FLAGS register")
                    sys.exit()

                elif l1[1] not in reg and l1[2] not in reg:
                    print("Error: Typos in register name")
                    sys.exit()

                elif l1[2] not in var:
                    print("Error: Use of undefined variables")
                    sys.exit()
                elif l1[2] in labels:
                    print("Error:  Misuse of variables as labels")
                    sys.exit()

                else:
                    dollars = l1[2].replace("$", "").replace(",", "")
                    dollars = int(dollars)

                    bin_val = DeciToBin(dollars)
                    bin_val = str(bin_val)

                    t = (8 - len(bin_val))

                    print_B(l1, t)
                    print(DeciToBin(dollars))

            # Type B mov: mov R1 $10
            if l1[0] == "mov" and l1[2] not in reg_val and l1[2] != "FLAGS":
                if len(l1) != 3:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                elif l1[1] == 'FLAGS':
                    print("Error: Illegal use of FLAGS register")
                    sys.exit()
                else:
                    dollars = l1[2].replace("$", "").replace(",", "")
                    dollars = int(dollars)

                    bin_val = DeciToBin(dollars)
                    bin_val = str(bin_val)

                    t = (8 - len(bin_val))

                    print_B_mov(l1, t)
                    print(DeciToBin(dollars))

            # Type C mov: mov R1 R2
            if l1[0] == "mov" and (l1[2] in reg_val or l1[2] == "FLAGS"):
                if len(l1) != 3:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                elif l1[1] == 'FLAGS':
                    print("Error: Illegal use of FLAGS register")
                    sys.exit()

                elif l1[1] not in reg and l1[2] not in reg:
                    print("Error: Typos in register name")
                    sys.exit()
                else:
                    if l1[2] in reg_val:
                        reg_val[l1[1]] = reg_val[l1[2]]
                    else:
                        reg_val[l1[1]] = BinToDeci(str(FLAG))
                    print_C_mov(l1)

            # Type C
            if l1[0] == "div" or l1[0] == "not" or l1[0] == "cmp":
                if len(l1) != 3:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                elif l1[1] == 'FLAGS' or l1[2] == 'FLAGS':
                    print("Error: Illegal use of FLAGS register")
                    sys.exit()
                elif l1[1] not in reg and l1[2] not in reg:
                    print("Error: Typos in register name")
                    sys.exit()
                else:
                    if l1[0] == "cmp":
                        calc_cmp(l1)
                    print_C(l1)

            # Type D
            if l1[0] == "ld" or l1[0] == "st":
                if len(l1) != 3:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                elif l1[1] == 'FLAGS':
                    print("Error: Illegal use of FLAGS register")
                    sys.exit()

                elif l1[1] not in reg:
                    print("Error: Typos in register name")
                    sys.exit()


                else:
                    bin_val = DeciToBin(len(instructions) - count_var + var[l1[2]])
                    bin_val = str(bin_val)

                    t = (8 - len(bin_val))

                    print_D(l1, t)
                    print(DeciToBin(len(instructions) - count_var + var[l1[2]]))

            # Type E jgt mylabel
            if l1[0] == "jmp" or l1[0] == "jlt" or l1[0] == "jgt" or l1[0] == "je":
                if len(l1) != 2:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                elif l1[1] == 'FLAGS':
                    print("Error: Illegal use of FLAGS register")
                    sys.exit()
                elif l1[1] not in labels and l1[1] != "label":
                    print("Error: Use of undefined labels")
                    sys.exit()
                elif l1[1] in var:
                    print("Error:  Misuse of labels as variables")
                    sys.exit()
                else:

                    bin_val = DeciToBin(
                        labels[l1[1]] - count_var)  # labels[l1[1]] --> line number at which that label is
                    bin_val = str(bin_val)

                    t = (8 - len(bin_val))

                    print_E(l1, t)
                    print(DeciToBin(labels[l1[1]] - count_var))


            # Type F
            if l1[0] == "hlt":
                if len(l1) != 1:
                    print("Error: Wrong syntax used for instructions")
                    sys.exit()
                else:
                    print_F(l1)
