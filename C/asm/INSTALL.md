# Requirements

`$ sudo aptitude install libc6-dev-i386 -ry`

# Assemble & link an asm 32-bits program

```
$ ld -m32 hello.o
ld: mode d'émulation non reconnu: 32
Émulations supportées: elf_x86_64 elf32_x86_64 elf_i386 i386linux elf_l1om elf_k1om i386pep i386pe
$ ld -melf_i386 hello.o
$ ls -lht
total 28K
-rwxr-xr-x 1 user user  668 oct.  30 19:49 a.out
-rw-r--r-- 1 user user  624 oct.  30 19:47 hello.o
...
-rw-r--r-- 1 user user  821 oct.  30 17:37 hello.asm
$ ./a.out 
Hello, world!
```