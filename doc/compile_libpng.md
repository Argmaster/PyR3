# Compiling libpng with -fPIC

```bash
user@user_pc:~/Documents$ mkdir libpng
user@user_pc:~/Documents$ cd libpng
user@user_pc:~/Documents/libpng$ wget https://download.sourceforge.net/libpng/libpng-1.6.37.tar.gz
user@user_pc:~/Documents/libpng$ tar xvfz libpng-1.6.37.tar.gz
user@user_pc:~/Documents/libpng$ cd libpng-1.6.37
user@user_pc:~/Documents/libpng/libpng-1.6.37$./configure --prefix=/home/user/Documents/libpng --with-pic=yes
user@user_pc:~/Documents/libpng/libpng-1.6.37$ sudo make
```
Your binaries are in `~/Documents/libpng/libpng-1.6.37/lib`, most interesting one is `libpng.a` which was now compiled with -fPIC.