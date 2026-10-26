#include <glad/glad.h>
#include "shader.h"
#include <stdio.h>

const char* vertex_shader_src = 
"#version 330 core\n"
"layout(location = 0) in vec4 vertex;\n"
"out vec2 TexCoords;\n"
"uniform mat4 projection;\n"
"void main(void){\n"
"     gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);\n"
"     TexCoords = vertex.zw;\n"
"}";

const char* fragment_shader_src =
"#version 330 core\n"
"in vec2 TexCoords;\n"
"out vec4 color;\n"
"uniform sampler2D text;\n"
"uniform vec3 textcolor;\n"
"void main(void){\n"
"     float alpha;\n"
"     alpha = texture(text, TexCoords).r;\n"
"     color = vec4(textcolor, alpha);\n"
"}";

 GLuint compile_text_shader(GLenum type, const char* src){
  GLuint shader;
  shader = glCreateShader(type);
  glShaderSource(shader, 1, &src, NULL);
  glCompileShader(shader);
  GLint success;
  glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
  if (!success){
    char info[512];
    glGetShaderInfoLog(shader, 512, 0, info);
    fprintf(stderr, "Shader Compile Error: %s\n", info);
  }
  return shader;
}


