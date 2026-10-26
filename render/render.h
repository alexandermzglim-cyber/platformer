#ifndef render_h 
#define render_h 
#include "../player/player.h"
#include "../camera/camera.h"

typedef struct GLFWwindow GLFWwindow;

void render_init(GLFWwindow* window, camera_info *camera);

//static void draw_player(player_info *p);

//static void draw_ground(int window_x, camera_info* camera);

void render_menu(void);

void render_levels(void);

void render_pause(void);

void render_level_completed(void);

void render_update(player_info *p, camera_info* camera, int window_x, int window_y);

#endif
