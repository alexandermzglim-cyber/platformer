CC = gcc
SRC = main.c math/vector.c player/player.c camera/camera.c input/input.c render/render.c glad/src/glad.c shader/text_shader/shader.c shader/main_game_shader/shader.c ttf/ttf_rendering.c level_loading/level_loader.c

CFLAGS = -Iglad/include -g

LIBS = -lglfw3 -lm -lopengl32 -lgdi32

platformer.exe: $(SRC)
	$(CC) $(SRC) $(CFLAGS) $(LIBS) -o platformer.exe

run: platformer.exe
	./platformer.exe

clean:
	del platformer.exe
