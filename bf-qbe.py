import argparse

def main():
    parser = argparse.ArgumentParser(
                        prog='BF QBE',
                        description='Compiles BF into QBE IR',
                        epilog='GOTTA GO FAST!')
    parser.add_argument('filename')
    args = parser.parse_args()
    prog = None
    with open(args.filename) as file:
        prog = file.read()
    bStack = []
    bCount = 0
    ir = '''# BF
# 30,000 bytes init to 0
data $a = { z 30000 }

export function w $main() {
@start
    %i =l add $a, 0
'''
    for op in prog:
        if op == '>':
            ir += '    %i =l add %i, 1\n'
        elif op == '<':
            ir += '    %i =l sub %i, 1\n'
        elif op == '+':
            ir += '    %temp =w loadsb %i\n'
            ir += '    %temp =w add %temp, 1\n'
            ir += '    storeb %temp, %i\n'
        elif op == '-':
            ir += '    %temp =w loadsb %i\n'
            ir += '    %temp =w sub %temp, 1\n'
            ir += '    storeb %temp, %i\n'
        elif op == '.':
            ir += '    %temp =w loadsb %i\n'
            ir += '    call $putchar(w %temp)\n'
        elif op == ',':
            ir += '    %char =l call $getchar()\n'
            # ir += '    %temp =w loadsb %char\n'
            ir += '    storeb %char, %i\n'
        elif op == '[':
            bStart = '@bstart' + str(bCount)
            bEnd = '@bend' + str(bCount)
            bCheck = '@bcheck' + str(bCount)
            bStack.append(bEnd)
            bStack.append(bCheck)
            bCount += 1
            ir += '    ' + bCheck + '\n'
            ir += '    %temp =w loadsb %i\n'
            ir += '    jnz %temp, ' + bStart + ', ' + bEnd + '\n'
            ir += '    ' + bStart + '\n'
        elif op == ']':
            bCheck = bStack.pop()
            bEnd = bStack.pop()
            ir += '    jmp ' + bCheck + '\n'
            ir += '    ' + bEnd + '\n'
    ir += '''    ret 0
}
    '''
    with open("file.ssa", "w") as file:
        file.write(ir)

if __name__ == '__main__':
    main()
