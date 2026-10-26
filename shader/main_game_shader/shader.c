#include <glad/glad.h>
#include <stddef.h>
#include "shader.h"
#include <stdio.h>

const char* vertex_shader_source =
"#version 330 core\n"
"layout (location = 0) in vec2 aPos;\n"
"uniform vec2 camera;\n"
"uniform float zoom;\n"
"uniform vec2 window;\n"
"\n"
"void main()\n"
"{\n"
"    vec2 pos = (aPos - camera) * zoom;\n"
"\n"
"    pos.x = (pos.x / window.x) * 2.0 - 1.0;\n"
"    pos.y = 1.0 - (pos.y / window.y) * 2.0;\n"
"\n"
"    gl_Position = vec4(pos, 0.0, 1.0);\n"
"}\n";

const char* fragment_shader_source =
"#version 330 core\n"
"out vec4 FragColor;\n"
"uniform vec3 color;\n"
"\n"
"void main()\n"
"{\n"
"    FragColor = vec4(color, 1.0);\n"
"}\n";


GLuint compile_shader(GLenum type, const char* source){
  GLuint shader;
  shader = glCreateShader(type);
  glShaderSource(shader, 1, &source, NULL);
  glCompileShader(shader);
  GLuint success;
  glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
  if (!success){
    char info[512];
    glGetShaderInfoLog(shader, 512, 0, info);
    fprintf(stderr, "Shader Compile Error: %s\n", info);
  }
  return shader;
}
