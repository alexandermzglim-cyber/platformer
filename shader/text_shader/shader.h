#ifndef text_shader_h
#define text_shader_h

extern const char* vertex_shader_src;
extern const char* fragment_shader_src;

GLuint compile_text_shader(GLenum type, const char* src);
 
#endif
