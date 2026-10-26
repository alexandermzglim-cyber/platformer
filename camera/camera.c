#include "camera.h"

void camera_init(camera_info* camera, float zoom, int window_x, int window_y){
  (*camera).x = 0.0f;
  (*camera).y = 0.0f;
  (*camera).zoom = zoom;
  (*camera).zone_w = window_x / 4.0f;
  (*camera).zone_h = window_y / 6.0f;
}

void camera_update(camera_info* camera, player_info *p, int window_x, int window_y, float dt){
 // (*camera).y = (1 - dt) * (*camera).y - dt  * (*p).position.y;
 // (*camera).x = (1 - dt) * (*camera).x - dt  * (*p).position.x;
  float left;
  left = (*camera).x + (window_x  - (*camera).zone_w) / 2 / (*camera).zoom;
  float right;
  right = left + (*camera).zone_w / (*camera).zoom;
  float top;
  top = (*camera).y + (window_y - (*camera).zone_h) / 2 / (*camera).zoom;
  float bottom;
  bottom = top + (*camera).zone_h / (*camera).zoom;
  float target_x;
  target_x = (*camera).x;
  if ((*p).position.x < left){
    target_x -= left - (*p).position.x;
  }
  if ((*p).position.x > right){
    target_x += (*p).position.x - right;
  }
  float target_y;
  target_y = (*camera).y;
  if ((*p).position.y < top){
    target_y -= top - (*p).position.y;
  }
  if ((*p).position.y > bottom){
    target_y += (*p).position.y - bottom;
  }
  (*camera).x += (target_x - (*camera).x) * dt * 5.0f;
  (*camera).y += (target_y - (*camera).y) * dt * 5.0f;
}
