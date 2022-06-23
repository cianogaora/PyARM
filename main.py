import registers


def init_regs():
    regs = []
    for i in range(13):
        newReg = registers.Register()
        newReg.name = newReg.name + str(i)
        regs.append(newReg)

    cpsr = registers.Register()
    cpsr.name = "CPSR"
    cpsr.value = "0"
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


def startup():
    regs = init_regs()
    with open('demo.s') as f:
        instructions = f.readlines()
    labels = []
    for instruction in instructions:
        print(f"executing instruction {instruction}")
        if instruction == 'end':
            break

        elif instruction == '\n' or instruction[0] == ';':
            continue

        if instruction[-2] == ':':
            labels.append(instruction[0:-2])
            continue

        else:
            op = get_op(instruction)
            reg_num = get_reg_num(instruction)
            reg_digits = len(str(reg_num))

            first, second = 0, 0
            if op == 'mov' or op == 'MOV':
                if instruction[8] == '#':
                    value = instruction[9]
                    count = 10
                    while instruction[count].isnumeric():
                        value += instruction[count]
                        count += 1

                    value = int(value)
                    regs[reg_num].value = hex(value)

            if op == 'add' or op == 'ADD':

                if instruction[12] == 'r' or instruction[12] == 'R':
                    first = int(regs[int(instruction[9:9+reg_digits])].value, 16)
                    second = int(regs[int(instruction[13:13+reg_digits])].value, 16)

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
                result = hex(result)
                regs[reg_num].value = result

            if op == 'sub' or op == 'SUB':
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
                result = hex(first - second)
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

    print_regs(regs)


if __name__ == '__main__':
    startup()
