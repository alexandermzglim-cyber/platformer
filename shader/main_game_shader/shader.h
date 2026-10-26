#ifndef shader_h 
#define shader_h 
#include <glad/glad.h> 

extern const char* vertex_shader_source;
extern const char* fragment_shader_source;

GLuint compile_shader(GLenum type, const char* src);

#endif
