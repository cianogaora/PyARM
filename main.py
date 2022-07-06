import registers


def init_regs():
    regs = []
    for i in range(13):
        newReg = registers.Register(2 ** 32)
        newReg.name = newReg.name + str(i)
        regs.append(newReg)

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


def get_reg_num(instruction):
    reg_num = instruction[5]

    if instruction[6] != ',':
        reg_num += instruction[6]

    reg_num = int(reg_num)
    return reg_num


def print_regs(regs):
    count = 0
    for reg in regs:
        if count == 6:
            print(reg.name + ': ' + reg.value + '\n', end='')
            count += 1
            continue
        print(reg.name + ': ' + reg.value, end='  ')
        count += 1
    print('\n')


def startup(filename):
    regs = init_regs()
    neg_idx = 13
    zero_idx = 14
    overflow_idx = 15
    carry_idx = 16
    line_num = 1
    with open(filename) as f:
        instructions = f.readlines()
    labels = []
    for instruction in instructions:

        if instruction == 'end':
            return

        elif instruction == '\n' or instruction[0] == ';':
            line_num += 1
            continue

        if instruction[-2] == ':':
            labels.append(instruction[0:-2])
            line_num += 1
            continue

        else:
            print(f"executing instruction {instruction}") 
            op = get_op(instruction)
            reg_num = get_reg_num(instruction)
            reg_digits = len(str(reg_num))
            reg1 = regs[int(instruction[9:9 + reg_digits])]

            first, second = 0, 0
            if op == 'mov' or op == 'MOV':
                if instruction[8] == '#':
                    value = instruction[9]
                    count = 10
                    while instruction[count].isnumeric():
                        value += instruction[count]
                        count += 1

                    value = int(value)
                    if value > reg1.max:
                        value = reg1.max
                        regs[reg_num].value = hex(value)
                        print(f"value too high on line {line_num}")
                        return
                    regs[reg_num].value = hex(value)

            if op == 'add' or op == 'ADD':

                if instruction[12] == 'r' or instruction[12] == 'R':
                    first = int(regs[int(instruction[9:9 + reg_digits])].value, 16)
                    second = int(regs[int(instruction[13:13 + reg_digits])].value, 16)

                elif instruction[12] == '#':
                    first = int(regs[int(instruction[9])].value, 16)
                    second = instruction[13]
                    count = 14
                    while instruction[count].isnumeric():
                        second += (instruction[count])

                    second = int(second)
                result = hex(first + second)
                regs[reg_num].value = result

            if op == 'mul' or op == 'MUL':


                if instruction[12] == 'r' or instruction[12] == 'R':
                    first = int(regs[int(instruction[9:9 + reg_digits])].value, 16)
                    second = int(regs[int(instruction[13:13 + reg_digits])].value, 16)

                elif instruction[12] == '#':
                    first = int(regs[int(instruction[9])].value, 16)
                    second = instruction[13]
                    count = 14
                    while instruction[count].isnumeric():
                        second += (instruction[count])
                    second = int(second)
                result = first * second
                # result = hex(result)

                if result > reg1.max:
                    result = reg1.max
                    regs[overflow_idx].value = "1"
                regs[reg_num].value = hex(result)

            if op == 'sub' or op == 'SUB':

                if instruction[12] == 'r' or instruction[12] == 'R':
                    reg2 = regs[int(instruction[13:13 + reg_digits])]
                    first = int(reg1.value, 16)
                    second = int(reg2.value, 16)

                elif instruction[12] == '#':
                    first = int(regs[int(instruction[9])].value, 16)
                    second = instruction[13]
                    count = 14
                    while instruction[count].isnumeric():
                        second += (instruction[count])
                    second = int(second)

                result = hex(first - second)
                if first - second < 0:
                    result = hex(reg1.max - second - first)
                    regs[neg_idx].value = "1"
                regs[reg_num].value = result

            if op == 'and' or op == 'AND':
                if instruction[12] == 'r' or instruction[12] == 'R':
                    first = int(regs[int(instruction[9:9 + reg_digits])].value, 16)
                    second = int(regs[int(instruction[13:13 + reg_digits])].value, 16)

                elif instruction[12] == '#':
                    first = regs[int(instruction[9])].value
                    second = instruction[13]
                    count = 14
                    while instruction[count].isnumeric():
                        second += (instruction[count])
                    second = int(second)
                result = hex(first & second)
                regs[reg_num].value = result

            if op == 'orr' or op == 'ORR':
                if instruction[12] == 'r' or instruction[12] == 'R':
                    first = int(regs[int(instruction[9:9 + reg_digits])].value, 16)
                    second = int(regs[int(instruction[13:13 + reg_digits])].value, 16)

                elif instruction[12] == '#':
                    first = regs[int(instruction[9])].value
                    second = instruction[13]
                    count = 14
                    while instruction[count].isnumeric():
                        second += (instruction[count])
                    second = int(second)

                result = hex(first | second)
                regs[reg_num].value = result

            if op == 'eor' or op == 'EOR':
                if instruction[12] == 'r' or instruction[12] == 'R':
                    first = int(regs[int(instruction[9:9 + reg_digits])].value, 16)
                    second = int(regs[int(instruction[13:13 + reg_digits])].value, 16)

                elif instruction[12] == '#':
                    first = regs[int(instruction[9])].value
                    second = instruction[13]
                    count = 14
                    while instruction[count].isnumeric():
                        second += (instruction[count])
                    second = int(second)

                result = hex(first ^ second)
                regs[reg_num].value = result
            line_num += 1

    print_regs(regs)


if __name__ == '__main__':
    filename = 'demo.s'
    startup(filename)
