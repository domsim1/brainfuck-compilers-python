import argparse

def main():
    parser = argparse.ArgumentParser(
                        prog='BF LLVM',
                        description='Compiles BF into LLVM IR',
                        epilog='GOTTA GO FAST!')
    parser.add_argument('filename')
    args = parser.parse_args()
    prog = None
    with open(args.filename) as file:
        prog = file.read()
    bStack = []
    bCount = 0
    ins = 1
    ir = '''@a = global [30000 x i8] zeroinitializer, align 16

define i32 @main() {
    %i = alloca i64, align 8
    store i64 0, ptr %i, align 4
'''
    for op in prog:
        if op == '>':
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %' + str(ins) + ' = add i64 %'+ str(ins - 1) + ', 1\n'
            ir += '    store i64 %'+ str(ins) + ', ptr %i, align 8\n'
            ins += 1
        elif op == '<':
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %' + str(ins) + ' = sub i64 %'+ str(ins - 1) + ', 1\n'
            ir += '    store i64 %'+ str(ins) + ', ptr %i, align 8\n'
            ins += 1
        elif op == '+':
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %'+ str(ins) + ' = getelementptr inbounds [30000 x i8], ptr @a, i64 0, i64 %' + str(ins- 1) + '\n'
            ins += 1
            ir += '    %'+ str(ins) +' = load i8, ptr %' + str(ins - 1) +', align 1\n'
            ins += 1
            ir += '    %' + str (ins) + ' = sext i8 %'+ str(ins - 1) +' to i32\n'
            ins += 1
            ir += '    %' + str(ins) + ' = add nsw i32 %'+ str(ins - 1) +', 1\n'
            ins += 1
            ir += '    %' + str(ins) + ' = trunc i32 %' +str(ins - 1) + ' to i8\n'
            ir += '    store i8 %' + str(ins) + ', ptr %' + str(ins - 4) + '\n'
            ins += 1
        elif op == '-':
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %'+ str(ins) + ' = getelementptr inbounds [30000 x i8], ptr @a, i64 0, i64 %' + str(ins- 1) + '\n'
            ins += 1
            ir += '    %'+ str(ins) +' = load i8, ptr %' + str(ins - 1) +', align 1\n'
            ins += 1
            ir += '    %' + str (ins) + ' = sext i8 %'+ str(ins - 1) +' to i32\n'
            ins += 1
            ir += '    %' + str(ins) + ' = sub nsw i32 %'+ str(ins - 1) +', 1\n'
            ins += 1
            ir += '    %' + str(ins) + ' = trunc i32 %' +str(ins -1) + ' to i8\n'
            ir += '    store i8 %' + str(ins) + ', ptr %' + str(ins - 4) + '\n'
            ins += 1
        elif op == '.':
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %'+ str(ins) + ' = getelementptr inbounds [30000 x i8], ptr @a, i64 0, i64 %' + str(ins- 1) + '\n'
            ins += 1
            ir += '    %'+ str(ins) +' = load i8, ptr %' + str(ins - 1) +', align 1\n'
            ins += 1
            ir += '    %' + str(ins) + ' = sext i8 %'+ str(ins - 1) +' to i32\n'
            ins += 1
            ir += '    %' + str(ins) + ' = call i32 @putchar(i32 noundef %' + str(ins - 1) + ')\n'
            ins += 1
        elif op == ',':
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %'+ str(ins) + ' = getelementptr inbounds [30000 x i8], ptr @a, i64 0, i64 %' + str(ins- 1) + '\n'
            ins += 1
            ir += '    %'+ str(ins) + ' = call i32 @getchar()\n'
            ins += 1
            ir += '    %' + str(ins) + ' = trunc i32 %' + str(ins - 1) + ' to i8\n'
            ins += 1
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %'+ str(ins) + ' = getelementptr inbounds [30000 x i8], ptr @a, i64 0, i64 %' + str(ins- 1) + '\n'
            ir += '    store i8 %' + str(ins - 2) + ', ptr %' + str(ins) + ', align 1 \n'
            ins += 1
        elif op == '[':
            ir += '    br label %l' + str(bCount) + '\n\n'
            ir += 'l' + str(bCount) + ':\n'
            bStack.append(bCount)
            bCount += 1
            ir += '    %' + str(ins) + ' = load i64, ptr %i, align 8\n'
            ins += 1
            ir += '    %'+ str(ins) + ' = getelementptr inbounds [30000 x i8], ptr @a, i64 0, i64 %' + str(ins- 1) + '\n'
            ins += 1
            ir += '    %'+ str(ins) +' = load i8, ptr %' + str(ins - 1) +', align 1\n'
            ins += 1
            ir += '    %' + str (ins) + ' = sext i8 %'+ str(ins - 1) +' to i32\n'
            ins += 1
            ir += '    %' + str(ins) + ' = icmp ne i32 %' + str(ins - 1) + ', 0\n'
            ins += 1
            ir += '    br i1 %' + str(ins - 1) + ', label %l' + str(bCount) + ', label %l' + str(bCount + 1) + '\n\n'
            ir += 'l' + str(bCount) + ': \n '
            bCount += 1
            bStack.append(bCount)
            bCount += 1
        elif op == ']':
            end = bStack.pop()
            start = bStack.pop()
            ir += '    br label %l' + str(start) + '\n\n'
            ir += 'l' + str(end) + ':\n'
    ir += '''    ret i32 0
}

declare i31 @putchar(i32 noundef) nounwind
declare i31 @getchar() nounwind
    '''
    with open("file.ll", "w") as file:
        file.write(ir)

if __name__ == '__main__':
    main()
