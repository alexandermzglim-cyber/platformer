#include "ttf_rendering.h"
#define STB_TRUETYPE_IMPLEMENTATION
#include "stb_truetype.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../shader/text_shader/shader.h"

#define FONT_BITMAP_SIZE 2048
static const int first_char = 32;
static const int last_char = 126;
static stbtt_fontinfo font;
static unsigned char* ttf_buffer = NULL;
static GLuint font_texture = 0;
static GLuint vao = 0;
static GLuint vbo = 0;
static GLuint shader_program = 0;
static stbtt_bakedchar cdata[96];

static void init_shader(void){
  GLuint vs = compile_text_shader(GL_VERTEX_SHADER, vertex_shader_src);
  GLuint fs = compile_text_shader(GL_FRAGMENT_SHADER, fragment_shader_src);
  shader_program = glCreateProgram();
  glAttachShader(shader_program, vs);
  glAttachShader(shader_program, fs);
  glLinkProgram(shader_program);
  GLint success;
  glGetProgramiv(shader_program, GL_LINK_STATUS, &success);
  if (!success){
    fprintf(stderr, "Shader Link Failed\n");
  }
  glDeleteShader(vs);
  glDeleteShader(fs);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

void ttf_load_font(const char* path, float pixel_height){
  FILE* fonts;
  fonts = fopen(path, "rb");
  if (!fonts){
    fprintf(stderr, "Cannot Open Font %s\n", path);
    return;
  }
  fseek(fonts, 0, SEEK_END);
  long size;
  size  = ftell(fonts);
  fseek(fonts, 0 , SEEK_SET);
  ttf_buffer = malloc(size);
  fread(ttf_buffer, 1, size, fonts);
  fclose(fonts);
  if(!stbtt_InitFont(&font, ttf_buffer, 0)){
    fprintf(stderr, "Failed to Initialise Font\n");
    return;
  }
  static unsigned char bitmap[FONT_BITMAP_SIZE * FONT_BITMAP_SIZE];
  stbtt_BakeFontBitmap(ttf_buffer, 0, pixel_height, bitmap, FONT_BITMAP_SIZE, FONT_BITMAP_SIZE, first_char, 96, cdata);
  glGenTextures(1, &font_texture);
  glBindTexture(GL_TEXTURE_2D, font_texture);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, FONT_BITMAP_SIZE, FONT_BITMAP_SIZE, 0, GL_RED, GL_UNSIGNED_BYTE, bitmap);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glGenVertexArrays(1, &vao);
  glGenBuffers(1, &vbo);
  glBindVertexArray(vao);
  glBindBuffer(GL_ARRAY_BUFFER, vbo);
  glBufferData(GL_ARRAY_BUFFER, sizeof(float) * 6 * 4 * 128, NULL, GL_DYNAMIC_DRAW);
  glEnableVertexAttribArray(0);
  glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * sizeof(float), 0);
  glBindBuffer(GL_ARRAY_BUFFER, 0);
  glBindVertexArray(0);
  init_shader();
}

void ttf_render_text(const char* text, float x, float y, float scale, float anchor_x, float anchor_y, float r, float g, float b){
  float text_width;
  text_width = 0;
  size_t len;
  len = strlen(text);
  for (size_t i = 0; i < len; i++){
    char c;
    c = text[i];
    if (c < first_char || c > last_char){
      continue;
    }
    stbtt_bakedchar bc;
    bc = cdata[c - first_char];
    text_width += bc.xadvance * scale;
  }
  x -= text_width * anchor_x;
  int ascent;
  int descent;
  int lineGap;
  stbtt_GetFontVMetrics(&font, &ascent, &descent, &lineGap);
  float text_height;
  text_height = (ascent - descent) * scale;
  glUseProgram(shader_program);
  GLint color_loc;
  color_loc = glGetUniformLocation(shader_program, "textColor");
  glUniform3f(color_loc, r, g, b);
  int width;
  int height;
  GLint viewport[4];
  glGetIntegerv(GL_VIEWPORT, viewport);
  width = viewport[2];
  height = viewport[3];
  y = height - y;
  y -= text_height * anchor_y;
  float projection[16] = {2.0f/width, 0, 0, 0, 0, -2.0f/height, 0, 0, 0, 0, -1, 0, -1, 1, 0, 1};
  GLint proj_loc;
  proj_loc = glGetUniformLocation(shader_program, "projection");
  glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection);
  glActiveTexture(GL_TEXTURE0);
  glBindTexture(GL_TEXTURE_2D, font_texture);
  glBindVertexArray(vao);
  float xpos;
  float ypos;
  xpos = x;
  ypos = y;
  for (size_t i = 0; i < len; i++){
    char c;
    c = text[i];
    if (c < first_char || c > last_char){
      continue;
    }
    stbtt_aligned_quad q;
    float x_before;
    x_before = xpos;
    float y_before;
    y_before = ypos;
    stbtt_GetBakedQuad(cdata, FONT_BITMAP_SIZE, FONT_BITMAP_SIZE, c - first_char, &xpos, &ypos, &q, 1);
    q.x0 = x_before + (q.x0 - x_before) * scale;
    q.x1 = x_before + (q.x1 - x_before) * scale;
    q.y0 = y_before + (q.y0 - y_before) * scale;
    q.y1 = y_before + (q.y1 - y_before) * scale; 
    float vertices [6][4] = {{q.x0, q.y1, q.s0, q.t1}, {q.x0, q.y0, q.s0, q.t0}, {q.x1, q.y0, q.s1, q.t0}, {q.x0, q.y1, q.s0, q.t1}, {q.x1, q.y0, q.s1, q.t0}, {q.x1, q.y1, q.s1, q.t1}};
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(vertices), vertices);
    glDrawArrays(GL_TRIANGLES, 0, 6);
  }
  glBindVertexArray(0);
  glBindTexture(GL_TEXTURE_2D, 0);
}

void ttf_free_font(void){
  if(ttf_buffer){
    free(ttf_buffer);
    ttf_buffer = NULL;
  }
  glDeleteTextures(1, &font_texture);
  glDeleteBuffers(1, &vbo);
  glDeleteVertexArrays(1, &vao);
  glDeleteProgram(shader_program);
}
