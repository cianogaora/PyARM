class ALU:
    def __init__(self):
        self.neg_idx = 13
        self.zero_idx = 14
        self.overflow_idx = 15
        self.carry_idx = 16

    def mov(self, instruction, regs, reg1, reg_num, line_num, conds):
        if not conds:
            if instruction[8] == '#':
                value = instruction[9]
                count = 10
                while instruction[count].isnumeric():
                    value += instruction[count]
                    count += 1

                value = int(value)
                if value > reg1.max:
                    value = reg1.max
                    print(f"value too high on line {line_num}")

                print(f"moving value {value} into reg {reg_num}")
                regs[reg_num].value = hex(value)
                print(regs[reg_num].value)
                print('')
                return
            else:
                reg2_num = instruction[9]
                count = 10
                while instruction[count].isnumeric():
                    reg2_num += instruction[count]
                    count += 1
                reg2_num = int(reg2_num)
                print(f"moving value {regs[reg2_num].value} into reg {reg_num}")
                val = regs[reg2_num].value
                regs[reg_num].value = val
                print('\n')
                return

        else:
            if instruction[9] == '#':
                value = instruction[10]
                count = 11
                while instruction[count].isnumeric():
                    value += instruction[count]
                    count += 1

                value = int(value)
                if value > reg1.max:
                    value = reg1.max
                    regs[reg_num].value = hex(value)
                    print(f"value too high on line {line_num}")

            else:
                reg2_num = instruction[9]
                count = 10
                while instruction[count].isnumeric():
                    reg2_num += instruction[count]
                    count += 1

                reg2_num = int(reg2_num)
                print(f"moving value {regs[reg2_num].value} into reg {reg_num}")
                regs[reg_num].value = regs[reg2_num].value
                print('\n')

            if value < 0:
                regs[self.neg_idx].value = '1'
            if value == 0:
                regs[self.zero_idx].value = '1'

            print(f"moving value {value} into reg {reg_num}")
            regs[reg_num].value = hex(value)
            print(regs[reg_num].value)
            print('')
            return

    def add(self, regs, first, second, reg1, reg_num, conds):
        result = hex(first + second)
        if conds:
            regs[self.overflow_idx].value = '0'
            regs[self.zero_idx].value = '0'
            regs[self.neg_idx].value = '0'
            regs[self.carry_idx].value = '1'
        if int(result, 16) > reg1.max:
            result = hex(int(result, 16) - reg1.max - 1)
            if conds:
                regs[self.overflow_idx].value = '1'

        print(f"moving value {result} into reg {reg_num}")
        regs[reg_num].value = result
        if int(result, 16) == 0 and conds:
            regs[self.zero_idx].value = '1'

        print(regs[reg_num].value)
        print('')

    def mul(self, regs, first, second, reg1, reg_num, conds):
        result = first * second
        if conds:
            regs[self.overflow_idx].value = '0'
            regs[self.zero_idx].value = '0'
            regs[self.neg_idx].value = '0'
            regs[self.carry_idx].value = '1'

        if result > reg1.max:
            result = reg1.max
            if conds:
                regs[self.overflow_idx].value = "1"

        print(f"moving value {result} into reg {reg_num}")
        regs[reg_num].value = hex(result)
        if result == 0 and conds:
            regs[self.zero_idx].value = '1'

        print(regs[reg_num].value)
        print('')

    def sub(self, regs, first, second, reg1, reg_num, conds):
        result = hex(first - second)
        if conds:
            regs[self.overflow_idx].value = '0'
            regs[self.zero_idx].value = '0'
            regs[self.neg_idx].value = '0'
            regs[self.carry_idx].value = '1'

        if first - second < 0:
            result = hex(reg1.max - abs(second - first) + 1)
            if conds:
                regs[self.neg_idx].value = "1"
                regs[self.carry_idx].value = "0"
        if first - second == 0 and conds:
            regs[self.zero_idx].value = '1'

        print(f"moving value {result} into reg {reg_num}")
        regs[reg_num].value = result
        print(regs[reg_num].value)
        print('')

    def bit_and(self, regs, first, second, reg_num, conds):
        result = hex(first & second)
        if conds:
            regs[self.overflow_idx].value = '0'
            regs[self.zero_idx].value = '0'
            regs[self.neg_idx].value = '0'
            regs[self.carry_idx].value = '1'

        print(f"moving value {result} into reg {reg_num}")
        regs[reg_num].value = result
        if result == 0 and conds:
            regs[self.zero_idx].value = '1'

        print(regs[reg_num].value)
        print('')

    def orr(self, regs, first, second, reg_num, conds):
        result = hex(first | second)
        if conds:
            regs[self.overflow_idx].value = '0'
            regs[self.zero_idx].value = '0'
            regs[self.neg_idx].value = '0'
            regs[self.carry_idx].value = '1'

        print(f"moving value {result} into reg {reg_num}")
        regs[reg_num].value = result
        if result == 0 and conds:
            regs[self.zero_idx].value = '1'

        print(regs[reg_num].value)
        print('')

    def eor(self, regs, first, second, reg_num, conds):
        result = hex(first ^ second)
        if conds:
            regs[self.overflow_idx].value = '0'
            regs[self.zero_idx].value = '0'
            regs[self.neg_idx].value = '0'
            regs[self.carry_idx].value = '1'

        print(f"moving value {result} into reg {reg_num}")
        regs[reg_num].value = result
        if result == 0 and conds:
            regs[self.zero_idx].value = '1'

        print(regs[reg_num].value)
        print('')

    def cmp(self, regs, first, second):
        result = first - second
        regs[self.overflow_idx].value = '0'
        regs[self.zero_idx].value = '0'
        regs[self.neg_idx].value = '0'
        regs[self.carry_idx].value = '1'

        if result == 0:
            regs[self.zero_idx].value = '1'
            return True
        else:
            if result < 0:
                regs[self.neg_idx].value = '1'
                regs[self.carry_idx].value = '0'
            return False

    def branch(self, label, labels):
        for item in labels:
            if item[0] == label:
                return item[1]

        print("Label not present in code")
        return "invalid"
