#ifndef input_h
#define input_h
#include <GLFW/glfw3.h>
#include "../player/player.h"
#include "../game.h"

extern bool level_confirmation;
static void key_callback(GLFWwindow*, int key, int scancode, int action, int mods);
void input_init(GLFWwindow* window, player_info *p, game_state* state);
void input_update(float dt);

#endif
