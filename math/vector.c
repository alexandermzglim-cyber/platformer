#include "vector.h"
#include <math.h>

vector1 vector_add(vector1 x, vector1 y){
  vector1 result;
  result = (vector1){x.x + y.x, x.y + y.y};
  return result;
}

vector1 vector_subtract(vector1 x, vector1 y){
  vector1 result;
  result = (vector1){x.x - y.x, x.y - y.y};
  return result;
}

vector1 vector_scale(vector1 v, float m){
  vector1 result;
  result = (vector1){v.x * m, v.y * m};
  return result;
}

float vector_length(vector1 v){
  float result;
  result = sqrtf(v.x * v.x + v.y * v.y);
  return result;
}

vector1 vector_normalise(vector1 v){
  float length;
  vector1 result;
  length = vector_length(v);
  if (length == 0){
    result = (vector1){0,0};
  } else{
    result = (vector1){v.x / length, v.y / length};
  }
  return result;
}

float vector_distance(vector1 x, vector1 y){
  float result;
  result = vector_length(vector_subtract(x, y));
  return result;
}

