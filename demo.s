;test mov
Stores:
movs r1, #1
mov r2, #2
MOV r1, #1
MOV r2, #2
mov r3, r2

;test addition
Adding:
add r3, r1, r2
add r4, r1, #1
ADD r3, r1, r2
ADD r4, r1, #1

;test mul
Multiply:
mov r5, #2
mul r5, r5, #2
mov r6, #2
mul r6, r6, r3

;test subtraction
Subtraction:
mov r1, #5
mov r2, #3
sub r3, r1, r2
mov r1, #5
sub r4, r1, #3

;test bitwise operations
;5 = 101, 6 = 110
;5 and 6 = 100 = 4
;5 or 6 = 111 = 7
;5 eor 6 = 011 = 3
Bitwise:
mov r1, #5
mov r2, #6
and r3, r1, r2
orr r4, r1, r2
eor r5, r1, r2

;>9
mov r8, #13

Flags:
;negative + carry
mov r1, #1
subs r1, #2

;overflow
mov r1, #4294967295
adds r1, #2

;zero and conds
mov r1, #4
subs r1, #4
mov r2, #2
muls r2, #0
mov r3, #0
adds r3, r3, r2

;branching
Branches:
mov r1, #2
mov r2, #2
cmp r1, r2
mov r2, #3
cmp r1, r2

;B Branches
mov r1, r2
cmp r1, r2
;beq Branches
mov r2, #3
cmp r1, r2
;assigning register values to others causing issues
blt Branches

end