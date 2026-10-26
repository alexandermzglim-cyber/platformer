#include "player.h"
#include <stdio.h>
#include "../level_loading/level_loader.h"
#include "../game.h"

static vector1 gravity = {0.0f, 2200.0f};
static const float movement_acceleration = 1900.0f;
static const float friction = 1500.0f;
static const float maximum_speed = 300.0f;
static const int TILE_SIZE = 16;
static const int player_width = 16;
static const int player_height = 16;

static bool check_solid(int x, int y){
  if (x < 0 || x >= max_level_width) return false;
  if (y < 0 || y >= max_level_height) return false;

  int tile = current_level[y][x];

  return (tile == 1);  // 1 = blockk
}

static bool check_spike(int x, int y){
  if (x < 0 || x >= max_level_width){
    return false;
  }
  if(y < 0 || y >= max_level_height){
    return false;
  }
  int spike;
  spike = current_level[y][x];
  return (spike == 2);
}

static bool check_checkpoint(int x, int y){
  if (x < 0 || x >= max_level_width){
    return false;
  }
  if (y < 0 || y >= max_level_height){
    return false;
  }
  int checkpoint;
  checkpoint = current_level[y][x];
  return (checkpoint == 4);
}

bool player_on_checkpoint(player_info *p){
  float center_x;
  center_x = (*p).position.x + player_width / 2;
  float center_y;
  center_y = (*p).position.y + player_height / 2;
  int tile_x;
  tile_x = (int)(center_x / TILE_SIZE);
  int tile_y;
  tile_y = (int)(center_y / TILE_SIZE);

}

bool player_on_spike(player_info *p){
  float center_x;
  center_x = (*p).position.x + player_width / 2;
  float center_y;
  center_y = (*p).position.y + player_height / 2;
  int tile_x;
  tile_x = (int)(center_x / TILE_SIZE);
  int tile_y;
  tile_y = (int)(center_y / TILE_SIZE);
  bool is_spike;
  is_spike = check_spike(tile_x, tile_y);
  return is_spike;
}

void player_init(player_info *p, vector1 start_position){
  (*p).position = start_position;
  (*p).velocity = (vector1){0.0f, 0.0f};
  (*p).ground = false;
  (*p).buffer_time = 0.0f;
  (*p).jump_held = false;
}

static void apply_gravity(player_info *p, float dt){
  float g_multiplier;
  g_multiplier = 1.0f;
  if ((*p).velocity.y > 0){
    g_multiplier = 1.5f;
  }
  vector1 g_force;
  g_force = vector_scale(gravity, dt * g_multiplier);
  (*p).velocity = vector_add((*p).velocity, g_force);
}

static void apply_friction(player_info *p, float dt){
  if ((*p).ground){
  if ((*p).velocity.x > 0){
    (*p).velocity.x -= friction * dt;
    if ((*p).velocity.x < 0){
      (*p).velocity.x = 0;
    }
  } else if ((*p).velocity.x < 0){
    (*p).velocity.x += friction * dt;
    if ((*p).velocity.x > 0){
      (*p).velocity.x = 0;
    }
   }
}
}

 static void change_collision_y(player_info *p, float dt){
  (*p).position.y += (*p).velocity.y * dt;
  (*p).ground = false;
  float left;
  left = (*p).position.x;
  float right;
  right = left + player_width;
  float top;
  top = (*p).position.y;
  float bottom;
  bottom = top + player_height;
  int tile_left;
  tile_left = (int)(left / TILE_SIZE);
  int tile_right;
  tile_right = (int)((right - 0.01f) / TILE_SIZE);
  int tile_top;
  tile_top = (int)(top / TILE_SIZE);
  int tile_bottom;
  tile_bottom = (int)((bottom - 0.01f) / TILE_SIZE);
  bool solidity;
  for (int y = tile_top; y < tile_bottom + 1; y++){
    for (int x = tile_left; x < tile_right + 1; x++){
      solidity = check_solid(x, y);
      if (!solidity){
        continue;
      }
      if ((*p).velocity.y > 0){
        (*p).position.y = y * TILE_SIZE - player_height;
        (*p).ground = true;
        (*p).jump_cut = false;
      }else if ((*p).velocity.y < 0){
        (*p).position.y = (y + 1) * TILE_SIZE;
      } 
      (*p).velocity.y = 0;
      break;
    }
    if ((*p).velocity.y == 0){
    break;
    }
  } 
} 

 /* static void change_collision_y(player_info *p, float dt){
    (*p).position.y += (*p).velocity.y * dt;

    float bottom = (*p).position.y + player_height;

    int tile_y = (int)(bottom / TILE_SIZE);
    int tile_left  = (int)((*p).position.x / TILE_SIZE);
    int tile_right = (int)(((*p).position.x + player_width - 0.001f) / TILE_SIZE);

    bool on_ground = false;

    for (int x = tile_left; x <= tile_right; x++){
        if (check_solid(x, tile_y)){

            if ((*p).velocity.y >= 0){
                (*p).position.y = tile_y * TILE_SIZE - player_height;
                (*p).velocity.y = 0;
                on_ground = true;
            }

            break;
        }
    }

    (*p).ground = on_ground;
}*/  

static void change_collision_x(player_info *p, float dt){
  (*p).position.x += (*p).velocity.x * dt;
  float left;
  left = (*p).position.x;
  float right;
  right = left + player_width;
  float top;
  top = (*p).position.y;
  float bottom;
  bottom = top + player_height;
  int tile_left;
  tile_left = (int)((left) / TILE_SIZE);
  int tile_right;
  tile_right = (int)((right - 0.01f) / TILE_SIZE);
  int tile_top;
  tile_top = (int)((top) / TILE_SIZE);
  int tile_bottom;
  tile_bottom = (int)((bottom - 0.01f) / TILE_SIZE);
  bool solidity;
  for (int y = tile_top; y <= tile_bottom; y++){
    for (int x = tile_left; x <= tile_right; x++){
      solidity = check_solid(x, y);
      if (!solidity){
        continue;
      }
      if ((*p).velocity.x > 0){
        (*p).position.x = x * TILE_SIZE - player_width;
      }else if ((*p).velocity.x < 0){
        (*p).position.x = (x + 1) * TILE_SIZE;
      }
      (*p).velocity.x = 0;
      break;
    }
    if ((*p).velocity.x == 0){
      break;
    }
  }
}


static void cyte_handler(player_info *p, float dt){
  if ((*p).ground){
    (*p).cyte_time = 0.1f;
  } else{
    (*p).cyte_time -= dt;
    if ((*p).cyte_time < 0){
      (*p).cyte_time = 0;
    }
  }
}

static void jump_buffer(player_info *p){
    if (((*p).ground || (*p).cyte_time > 0.0f) && (*p).buffer_time > 0.0f){
    (*p).velocity.y = -550.0f;
    (*p).ground = false;
    (*p).cyte_time = 0.0f;
    (*p).buffer_time = 0.0f;
  }
}

void release_jump(player_info *p){
  (*p).jump_held = false;
}

static void variable_jump(player_info *p){
  if (!(*p).jump_held && (*p).velocity.y < 0 && !(*p).jump_cut){
    (*p).velocity.y *= 0.5f;
    (*p).jump_cut = true;
  }
}

static float smooth_approach(float current_position, float target_position, float step){
  if (current_position < target_position){
    current_position += step;
    if (current_position > target_position){
      current_position = target_position;
    }
  } else if (current_position > target_position){
    current_position -= step;
    if (current_position < target_position){
      current_position = target_position;
    }
  }
  return current_position;
}

static void buffer_fix(player_info *p, float dt){
  (*p).buffer_time -= dt;
  if ((*p).buffer_time < 0){
    (*p).buffer_time = 0;
  }
}

void player_update(player_info *p, float dt){
  bool was_grounded;
  was_grounded = (*p).ground;
  (*p).ground = false;
  apply_gravity(p, dt);
  variable_jump(p);
  jump_buffer(p);
  change_collision_x(p, dt);
  change_collision_y(p, dt);
  apply_friction(p, dt);
  cyte_handler(p, dt);
  buffer_fix(p, dt);
  if (player_on_goal(p)){
    level_completed = true;
  }
}

bool check_goal(int x, int y){
  if (x < 0 || x >= max_level_width){
    return false;
  }
  if (y < 0 || y >= max_level_height){
    return false;
  }
  if (current_level[y][x] == 3){
    return true;
  }
  else {
    return false;
  }
}

bool player_on_goal(player_info *p){
  float center_x;
  center_x = (*p).position.x + player_width / 2;
  float center_y;
  center_y = (*p).position.y + player_height / 2;
  int tile_x;
  tile_x = (int)(center_x / TILE_SIZE);
  int tile_y;
  tile_y = (int)(center_y / TILE_SIZE);
  bool on_goal;
  on_goal = check_goal(tile_x, tile_y);
  return on_goal;
}


void player_jump(player_info *p){
  (*p).buffer_time = 0.1f;
  (*p).jump_held = true;
  (*p).jump_cut = false;
}

void player_move_right(player_info *p, float dt){
  float multiplier;
  multiplier = 1.0f;
  if(!(*p).ground){
    multiplier = 0.5f;
  }
  (*p).velocity.x = smooth_approach((*p).velocity.x, maximum_speed, movement_acceleration * dt * multiplier);
}

void player_move_left(player_info *p, float dt){
  float multiplier;
  multiplier = 1.0f;
  if (!(*p).ground){
    multiplier = 0.5f;
  }
  (*p).velocity.x = smooth_approach((*p).velocity.x, -maximum_speed, movement_acceleration * dt * multiplier); 
}

//void player_stop(player_info *p){
// (*p).velocity.x = 0;
//}
