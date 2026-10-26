#ifndef camera_h 
#define camera_h

#include "../player/player.h"

typedef struct{
  float x;
  float y;
  float zoom;
  float zone_w;
  float zone_h;
} camera_info;

void camera_init(camera_info* camera, float zoom, int window_x, int window_y);
void camera_update(camera_info* camera, player_info *p, int window_x, int window_y, float dt);

#endif
