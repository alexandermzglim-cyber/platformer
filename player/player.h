#ifndef player_h 
#define player_h 

#include "../math/vector.h"

typedef struct {
  vector1 position;
  vector1 velocity;
  bool ground;
  float cyte_time;
  float buffer_time;
  bool jump_held;
  bool jump_cut;
} player_info;


void player_init(player_info *p, vector1 start_position);

static void apply_gravity(player_info *p, float t);

static void apply_friction(player_info *p, float t);

bool player_on_spike(player_info *p);

static void movement(player_info *p, float t);

static void change_collision_x(player_info *p, float dt);

static void change_collision_y(player_info *p, float dt);

static void cyte_handler(player_info *p, float t);

static void jump_buffer(player_info *p);

void release_jump(player_info *p);

static void variable_jump(player_info *p);

static float smooth_approach(float current_position, float target_position, float step);

void player_update(player_info *p, float t);

bool player_on_goal(player_info *p);

void player_jump(player_info *p);

void player_move_right(player_info *p, float t);

void player_move_left(player_info *p, float t);

void player_stop(player_info *p);

#endif

