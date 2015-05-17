# gcc

compile main.c (default executable output is a.out)

    gcc main.c


compile main.c into an outfile file main.o

    gcc main.c -o main.o


compile main.c and enable all warnings

    gcc -Wall main.c


compile main.c but do not run the linker

    gcc -c main.c


do not compile, only run the linker

    gcc main.o


compile with maximum optimization level (O as in optimize)

    gcc -O3 main.c


compile with size optimization enabled (O as in optimize)

    gcc -Os main.c


assemble main.c (default output is main.s)

    gcc -S main.c



# Basic Usage

Compile a file using the GNU compiler:

    gcc <file>



# Note

`gcc` can be replaced by `g++` to compile C++ files. It can also be replaced by
`clang` and `clang++` to use the Clang compiler instead, which has the same
command line interface.


