import registers
import alu

neg_idx = 13
zero_idx = 14
overflow_idx = 15
carry_idx = 16


def init_regs():
    regs = []
    for i in range(13):
        new_reg = registers.Register((2 ** 32) - 1)
        new_reg.name = new_reg.name + str(i)
        regs.append(new_reg)

    neg = registers.Register(1)
    neg.name = "NEGATIVE"
    neg.value = "0"
    regs.append(neg)

    zero = registers.Register(1)
    zero.name = "ZERO"
    zero.value = "0"
    regs.append(zero)

    overflow = registers.Register(1)
    overflow.name = "OVERFLOW"
    overflow.value = "0"
    regs.append(overflow)

    carry = registers.Register(1)
    carry.name = "CARRY"
    carry.value = "0"
    regs.append(carry)

    return regs


def get_op(instruction):
    op_len = 0
    for character in instruction:
        if character != ' ':
            op_len += 1
        else:
            op = instruction[0:op_len]
            return op


def get_reg_num(instruction, op_len):
    if op_len == 3:
        reg_num = instruction[5]
        if instruction[6] != ',':
            reg_num += instruction[6]

    elif op_len == 4:
        reg_num = instruction[6]
        if instruction[7] != ',':
            reg_num += instruction[7]
    else:
        print("invalid op")
        return

    reg_num = int(reg_num, 16)
    return reg_num


def print_regs(regs):
    count = 0
    for reg in regs:
        if count == 6:
            print(reg.name + ': ' + reg.value + '\n', end='')
            count += 1
            continue
        if count == 13:
            print('')

        print(reg.name + ': ' + reg.value, end='  ')
        count += 1
    print('\n')


def startup(filename):
    regs = init_regs()
    line_num = 1
    ALU = alu.ALU()
    with open(filename) as f:
        instructions = f.readlines()
    labels = []
    for instruction in instructions:

        if instruction == 'end':
            print_regs(regs)
            return

        elif instruction == '\n' or instruction[0] == ';':
            line_num += 1
            continue

        if instruction[-2] == ':':
            labels.append(instruction[0:-2])
            line_num += 1
            continue

        else:
            print(f"executing instruction {instruction[0:-1]}")
            op = get_op(instruction)
            reg_num = get_reg_num(instruction, len(op))
            op = op[0:3]
            reg_digits = len(str(reg_num))
            second = ''
            conds = False

            if instruction[3] == 's' or instruction[3] == 'S':
                conds = True

            if not conds:
                if instruction[8] != '#':
                    reg1 = regs[int(instruction[9:9 + reg_digits])]
                    first = int(reg1.value, 16)
                else:
                    reg1 = regs[reg_num]
                    first = int(reg1.value, 16)
                    count = 9
                    while instruction[count].isnumeric():
                        second += instruction[count]
                        count += 1
                    second = int(second)

                if len(instruction) >= 13:
                    if instruction[12] == 'r' or instruction[12] == 'R':
                        reg2 = regs[int(instruction[13:13 + reg_digits])]
                        second = int(reg2.value, 16)

                if len(instruction) >= 13:
                    if instruction[12] == 'r' or instruction[12] == 'R':
                        reg2 = regs[int(instruction[13:13 + reg_digits])]
                        second = int(reg2.value, 16)
            else:
                if instruction[9] != '#':
                    reg1 = regs[int(instruction[10:10 + reg_digits])]
                    first = int(reg1.value, 16)
                else:
                    reg1 = regs[reg_num]
                    first = int(reg1.value, 16)
                    count = 10
                    while instruction[count].isnumeric():
                        second += instruction[count]
                        count += 1
                    second = int(second)

                if len(instruction) >= 14:
                    if instruction[13] == 'r' or instruction[13] == 'R':
                        reg2 = regs[int(instruction[14:14 + reg_digits])]
                        second = int(reg2.value, 16)

            if op == 'mov' or op == 'MOV':
                ALU.mov(instruction, regs, reg1, reg_num, line_num, conds)

            if op != 'mov' and op != 'MOV':
                if len(instruction) >= 13:
                    if instruction[12] == '#':
                        second = instruction[13]
                        count = 14
                        while instruction[count].isnumeric():
                            second += (instruction[count])
                        second = int(second)

            if op == 'add' or op == 'ADD' or op == 'adc' or op == 'ADC':
                ALU.add(regs, first, second, reg1, reg_num, conds)
                if op == 'adc' or op == 'ADC':
                    regs[reg_num] += regs[carry_idx].value

            if op == 'mul' or op == 'MUL':
                ALU.mul(regs, first, second, reg1, reg_num, conds)

            if op == 'sub' or op == 'SUB':
                ALU.sub(regs, first, second, reg1, reg_num, conds)

            if op == 'and' or op == 'AND':
                ALU.bit_and(regs, first, second, reg_num, conds)

            if op == 'orr' or op == 'ORR':
                ALU.orr(regs, first, second, reg_num, conds)

            if op == 'eor' or op == 'EOR':
                ALU.eor(regs, first, second, reg_num, conds)

            if op == 'cmp' or op == 'CMP':
                pass

            line_num += 1


if __name__ == '__main__':
    filename = 'demo.s'
    startup(filename)
