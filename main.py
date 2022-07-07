import registers


def init_regs():
    regs = []
    for i in range(13):
        new_reg = registers.Register((2 ** 32)-1)
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
            print(f"executing instruction {instruction}")
            op = get_op(instruction)
            reg_num = get_reg_num(instruction)
            reg_digits = len(str(reg_num))
            second = ''
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
                    print(f"moving value {value} into reg {reg_num}")
                    regs[reg_num].value = hex(value)
                    print(regs[reg_num].value)
                    print('\n')

            if op != 'mov' and op != 'MOV':
                if len(instruction) >= 13:
                    if instruction[12] == '#':
                        second = instruction[13]
                        count = 14
                        while instruction[count].isnumeric():
                            second += (instruction[count])
                        second = int(second)

            if op == 'add' or op == 'ADD':
                result = hex(first + second)
                if int(result, 16) > reg1.max:
                    result = hex(int(result, 16) - reg1.max - 1)
                    regs[overflow_idx].value = '1'

                print(f"moving value {result} into reg {reg_num}")
                regs[reg_num].value = result
                if result == 0:
                    regs[zero_idx].value = '1'
                print(regs[reg_num].value)
                print('\n')

            if op == 'mul' or op == 'MUL':
                result = first * second

                if result > reg1.max:
                    result = reg1.max
                    regs[overflow_idx].value = "1"
                print(f"moving value {result} into reg {reg_num}")
                regs[reg_num].value = hex(result)
                if result == 0:
                    regs[zero_idx].value = '1'
                print(regs[reg_num].value)
                print('\n')

            if op == 'sub' or op == 'SUB':
                result = hex(first - second)
                regs[neg_idx].value = "1"

                if first - second < 0:
                    result = hex(reg1.max - second - first)
                    regs[neg_idx].value = "0"

                print(f"moving value {result} into reg {reg_num}")
                regs[reg_num].value = result
                if result == 0:
                    regs[zero_idx].value = '1'
                print(regs[reg_num].value)
                print('\n')

            if op == 'and' or op == 'AND':
                result = hex(first & second)
                print(f"moving value {result} into reg {reg_num}")
                regs[reg_num].value = result
                if result == 0:
                    regs[zero_idx].value = '1'
                print(regs[reg_num].value)
                print('\n')

            if op == 'orr' or op == 'ORR':
                result = hex(first | second)
                print(f"moving value {result} into reg {reg_num}")
                regs[reg_num].value = result
                if result == 0:
                    regs[zero_idx].value = '1'
                print(regs[reg_num].value)
                print('\n')

            if op == 'eor' or op == 'EOR':
                result = hex(first ^ second)
                print(f"moving value {result} into reg {reg_num}")
                regs[reg_num].value = result
                if result == 0:
                    regs[zero_idx].value = '1'
                print(regs[reg_num].value)
                print('\n')

            line_num += 1


if __name__ == '__main__':
    filename = 'demo.s'
    startup(filename)
