#include "input.h"
#include "../player/player.h"
#include "../game.h"
#include "../level_loading/level_loader.h"

static GLFWwindow* used_window;
static player_info* player_ptr;
static game_state* current_state; 
bool level_confirmation = false;

static void key_callback(GLFWwindow*, int key, int scancode, int action, int mods){
  if (*current_state == game_state_playing){
    if (action == GLFW_PRESS){
      switch (key){
        case GLFW_KEY_ESCAPE:
           *current_state = game_state_paused;    
        case GLFW_KEY_SPACE:
        case GLFW_KEY_W:
           player_jump(player_ptr);
           break;
      }
    }
    if (action == GLFW_RELEASE){
      switch (key){
        case GLFW_KEY_SPACE:
        case GLFW_KEY_W:
           release_jump(player_ptr);
      }
    }
  } else if (*current_state == game_state_menu){
  if (action == GLFW_PRESS){
    switch(key){
      case GLFW_KEY_UP:
         main_menu_selected--;
         if (main_menu_selected < 0){
          main_menu_selected = menu_count - 1;
         }
         break;
      case GLFW_KEY_DOWN:
         main_menu_selected++;
         if (main_menu_selected >= menu_count + 1){
          main_menu_selected = 0;
         }
         break;
      case GLFW_KEY_ENTER:
        switch(main_menu_selected){
          case menu_play:
             *current_state = game_state_level_select;
             break;
          case menu_editor:
             *current_state = game_state_editor;
             break;
          case menu_quit:
             glfwSetWindowShouldClose(used_window, 1);
        }
      break;
    }
  } 
} else if (*current_state == game_state_level_select){
    if (action == GLFW_PRESS){
      switch(key){
        case GLFW_KEY_UP:
           level_selected--;
           if (level_selected < 0){
            level_selected = 0;
           }
           break;
        case GLFW_KEY_DOWN:
           level_selected++;
           if (level_selected >= level_count){
            level_selected = 0;
           }
           break;
        case GLFW_KEY_ENTER:
           level_confirmation = true;
    //       *current_state = game_state_playing;
           break;
        case GLFW_KEY_ESCAPE:
           *current_state = game_state_menu;
           break;
      }
    }
  }
  else if (*current_state = game_state_paused){
    if (action == GLFW_PRESS){
      switch(key){
        case GLFW_KEY_UP:
           pause_selected--;
           if (pause_selected < 0){
            pause_selected = 3;
          }
          break;
        case GLFW_KEY_DOWN:
           pause_selected++;
           if (pause_selected > 3){
            pause_selected = 0;
          }
           break;
        case GLFW_KEY_ENTER:
           switch(pause_selected){
            case 0:
               *current_state = game_state_playing;
                break;
            case 1:
               *current_state = game_state_level_select;
               break;
            case 2:
               *current_state = game_state_menu;
               break;
            case 3:
               glfwSetWindowShouldClose(used_window, 1);
               break;
          }
          break;
        case GLFW_KEY_ESCAPE:
           *current_state = game_state_playing;
           break;
      }
    }
  }
  else if (*current_state == game_state_level_complete){
    if (action == GLFW_PRESS){
      if (key == GLFW_KEY_ENTER){
        *current_state = game_state_level_select;
      }
    }
  }
}

void input_init(GLFWwindow* window, player_info *p, game_state* state){
  used_window = window;
  player_ptr = p;
  current_state = state;
  glfwSetKeyCallback(window, key_callback);
}

void input_update(float dt){
  if (*current_state != game_state_playing){
    return;
  }
  if (glfwGetKey(used_window, GLFW_KEY_A) == GLFW_PRESS){
    player_move_left(player_ptr, dt);
  }
  if (glfwGetKey(used_window, GLFW_KEY_D) == GLFW_PRESS){
    player_move_right(player_ptr, dt);
  }
}

