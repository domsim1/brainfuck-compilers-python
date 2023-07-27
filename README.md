# Brainfuck Compilers Python

This is a quick experiment for testing QBE and LLVM with a naive brainfuck compiler.

`bf-qbe.py` will create a 'file.ssa' that can be compiled with QBE 1.1.

`bf-llvm.py` will create a 'file.ll' that can be compiled with LLVM 15.

Basic usage:

QBE
```
python bf-qbe.py test.b
qbe -o file.s file.ssa
cc file.s
./a.out
```

LLVM
```
python bf-llvm.py test.b
llc file.ll
cc file.s
./a.out
```

From testing QBE will fail to compile `LostKng.b`, it will use all avaliable RAM (around 13GB on my 16GB machine) and after 10 minutes will crash my terminal; LLVM on the other hand uses around 2GB of ram and works.

