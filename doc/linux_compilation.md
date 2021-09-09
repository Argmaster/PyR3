# Compiling blender as python module for Linux
## Tested on Ubuntu 20.04

*Compiling blender as python module on Linux turned out to be much trickier than i expected*.
*~Argmaster*

### Install Packages
```bash
user@user_pc:~$ sudo apt update
user@user_pc:~$ sudo apt install build-essential git subversion cmake libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libglew-dev
sudo apt install libwayland-dev wayland-protocols libegl-dev libxkbcommon-dev libdbus-1-dev linux-libc-dev
```
### Download Sources & libraries
0. Move to some work folder, for us it will be ~/Documents. Create *blender-git* folder for source files and *lib* folder for dependencies.
    ```bash
    user@user_pc:~$ cd Documents
    user@user_pc:~/Documents$ mkdir blender-git
    user@user_pc:~/Documents$ cd blender-git
    user@user_pc:~/Documents/blender-git$ mkdir lib
    ```
#### Following steps can be done concurrently, as they are independent and will take some time
1. **cd** into *blender-git* folder and clone blender repository
    ```bash
    user@user_pc:~/Documents/blender-git$ git clone https://git.blender.org/blender.git
    ```
2. *open new terminal window in `~/Documents/blender-git`* and **cd** into *lib* and download blender dependencies
    ```bash
    user@user_pc:~/Documents/blender-git$ cd lib
    user@user_pc:~/Documents/blender-git/lib$ svn checkout https://svn.blender.org/svnroot/bf-blender/tags/blender-2.93-release/lib/linux_centos7_x86_64
    ```
#### After git finishes downloading
3. **cd** into newly cloned blender source repository and change current branch to v2.93 release branch
    ```bash
    user@user_pc:~/Documents/blender-git$ cd blender
    user@user_pc:~/Documents/blender-git/blender$ git checkout blender-v2.93-release
    ```
#### Wait unitl svn (point 5.) finishes downloading and close it's terminal window

4. Ensure You have right libraries and sources by running
    ```bash
    user@user_pc:~/Documents/blender-git/blender$ make update
    ```
5. Open `~/Documents/blender-git/blender/CMakeLists.txt` in your favorite text editor. Find and change following options:
    - `WITH_MEM_JEMALLOC` to **OFF**
    - `WITH_AUDASPACE` make sure its **ON**
    - `WITH_PYTHON_INSTALL` to **OFF**
    - `WITH_PYTHON_MODULE` to **ON**

    *then save and quit.*
6. run make
    ```bash
    user@user_pc:~/Documents/blender-git/blender$ sudo make
    ```
    it should build all libraries, and it's very likely to fail with following error:
    ```
    /usr/bin/ld.gold: error: /usr/lib/x86_64-linux-gnu/libpng.a(pngerror.o): requires dynamic R_X86_64_PC32 reloc against 'stderr' which may overflow at runtime; recompile with -fPIC
    collect2: error: ld returned 1 exit status
    make[3]: *** [source/creator/CMakeFiles/blender.dir/build.make:534: bin/bpy.so] Error 1
    make[2]: *** [CMakeFiles/Makefile2:7272: source/creator/CMakeFiles/blender.dir/all] Error 2
    make[1]: *** [Makefile:163: all] Error 2
    make: *** [GNUmakefile:345: all] Error 2
    ```
    **if it does, it's "fine", we expected it.** If it didn't it's great, move to point 11. to see how to install compiled blender.
7. Error we encountered is caused by libpng.a not being compiled with -fPIC flag, it's somewhat explained [here](https://stackoverflow.com/questions/46980606/static-link-libpng-into-a-shared-library). The solution is to compile it yourself, or use version compiled with -fPIC.
8. To compile it yourself, see [compile libpng](https://github.com/Argmaster/pyr3/blob/main/doc/compile_libpng.md). For now we will use precompiled version. Download [libpng-with-pic-linux.tar.gz](https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries), for example into `~Documents/libpng` folder, and unpack it there.
9. Open new terminal window in `/usr/lib/x86_64-linux-gnu` and run
    ```bash
    user@user_pc:/usr/lib/x86_64-linux-gnu$ sudo mv libpng.a libpng_no_pic.a
    user@user_pc:/usr/lib/x86_64-linux-gnu$ sudo cp ~/Documents/libpng/lib/libpng.a libpng.a
    ```
    it will rename current libpng.a into libpng_no_pic.a and copy new libpng.a in its place.
10. Now we can again use our old terminal window form `~/Documents/blender-git/blender` and re-run make. It won't need to recompile all the dependencies, and should be pretty quick.
    ```bash
    user@user_pc:~/Documents/blender-git/blender$ sudo make
    ```
    If it succeeds, following file should exist: `~/Documents/blender-git/build_linux/bin/bpy.so` if it doesn't, it means that something has gone wrong.
11. Now you can see [install blender](https://github.com/Argmaster/pyr3/blob/main/doc/install_blender.md) Linux section for installation guidance.

