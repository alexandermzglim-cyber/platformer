# Windows Setup Guide

This project was built for Linux. Follow these steps to build and run it on Windows with VS Code.

## Step 1 — Install MSYS2

Download and install from **https://www.msys2.org**.

Open the **MSYS2 MINGW64** terminal and install the required packages:

```bash
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-make mingw-w64-x86_64-glfw
```

Then add `C:\msys64\mingw64\bin` to your Windows **PATH**:
- Open System Properties → Environment Variables
- Under "System variables", find `Path` and add `C:\msys64\mingw64\bin`

## Step 2 — Update the Makefile for Windows

Change the `LIBS` line in `makefile`:

```makefile
LIBS = -lglfw3 -lm -lopengl32 -lgdi32
```

Update the build target, run target, and clean target:

```makefile
platformer.exe: $(SRC)
	$(CC) $(SRC) $(CFLAGS) $(LIBS) -o platformer.exe

run: platformer.exe
	./platformer.exe

clean:
	del platformer.exe
```

## Step 3 — Install VS Code Extensions

Install these two extensions:

- **C/C++** by Microsoft (`ms-vscode.cpptools`) — IntelliSense and debugging
- **Makefile Tools** by Microsoft (`ms-vscode.makefile-tools`) — run make targets from VS Code

## Step 4 — Set the VS Code Terminal to MSYS2

In VS Code settings (`Ctrl+,`), set the default terminal to Git Bash or point it at the MSYS2 shell:

```json
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

Alternatively, set the shell path directly to `C:\msys64\mingw64.exe`.

## Step 5 — Build and Run

Open the terminal in VS Code and run:

```bash
make
./platformer.exe
```
