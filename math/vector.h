#ifndef vector_h 
#define vector_h 

typedef struct {
  float x;
  float y;
} vector1;

vector1 vector_add(vector1 x, vector1 y);
vector1 vector_subtract(vector1 x, vector1 y);
vector1 vector_scale(vector1 v, float m);
float vector_length(vector1 v);
vector1 vector_normalise(vector1 v);
float vector_distance(vector1 x, vector1 y);

#endif

