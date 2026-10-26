#include <GLFW/glfw3.h>
#include "player/player.h"
#include "input/input.h"
#include "render/render.h"
#include "camera/camera.h"
#include "game.h"
#include "level_loading/level_loader.h"

const int window_x = 3200;
const int window_y = 1500;
const double MAX_DT = 0.05;
int main_menu_selected = 0;
int level_selected = 0;
int level_count = 3;
int pause_selected = 0;
bool level_completed = false;
bool levels_completed[100] = {false};

void handle_level_complete(game_state *state){
  if (!level_completed){
    return;
  }
  level_completed = false;
  //free_level();
  levels_completed[level_selected] = true;
  *state = game_state_level_complete;
}

int main(void){
  game_state current_state;
  current_state = game_state_menu;
  if (!glfwInit()){
    return -1;
  }
  GLFWwindow* window;
  window = glfwCreateWindow(window_x, window_y, "Platformer Game", NULL, NULL);
  if (!window){
    glfwTerminate();
    return -1;
  }
  glfwMakeContextCurrent(window);
  camera_info camera;
  camera_init(&camera, 2.5f, window_x, window_y);
  player_info player;
  player_init(&player, (vector1){400.0f, 300.0f});
  input_init(window, &player, &current_state);
  render_init(window, &camera);
  double last_time;
  last_time = glfwGetTime();
  double current_time;
  double dt;
  int first_frame;
  first_frame = 1;
  while (!glfwWindowShouldClose(window)){
    glfwPollEvents();
    int focused;
    focused = glfwGetWindowAttrib(window, GLFW_FOCUSED);
    current_time = glfwGetTime();
    dt = current_time - last_time;
    if (!first_frame){
      bool focused;
      focused = glfwGetWindowAttrib(window, GLFW_FOCUSED);
      if (!focused){
        last_time = current_time;
        continue;
      }
    } else {
      first_frame = false;
    }
    if (dt > MAX_DT){
      dt = MAX_DT;
    }
    last_time = current_time;
    switch(current_state){
      case game_state_menu:
         render_menu();
         break;
      case game_state_level_select:
         render_levels();
         if (level_confirmation){
          free_level();
          load_level(level_selected);
          player_init(&player, (vector1){10.0f, 5.0f});
          level_confirmation = false;
          current_state = game_state_playing;
        }
         break;
      case game_state_playing:
         input_update((float)dt);
         player_update(&player, (float)dt);
         if (player_on_spike(&player) || player_fell_off_level(&player)){
          player_init(&player, (vector1){10.0f, 5.0f});
        }
         handle_level_complete(&current_state);
         camera_update(&camera, &player, window_x, window_y, (float)dt);
         render_update(&player, &camera, window_x, window_y);
         break;
      case game_state_paused:
         render_pause();
         break;
      case game_state_level_complete:
         render_level_completed();
         break;
      case game_state_editor:
         render_editor();
         break;
    }
    glfwSwapBuffers(window);
  }
  glfwDestroyWindow(window);
  glfwTerminate();
  return 0;
}
