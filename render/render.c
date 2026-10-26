#include <glad/glad.h>
#include "render.h"
#include <GLFW/glfw3.h>
#include <stddef.h>
#include "../player/player.h"
#include "../camera/camera.h"
#include "../shader/main_game_shader/shader.h"
#include "../ttf/ttf_rendering.h"
#include "../game.h"
#include <stdio.h>
#include "../level_loading/level_loader.h"

static GLFWwindow* window_reference;
static GLuint shader_program;
static GLuint vao;
static GLuint vbo;
const int TILE_SIZE = 16;
const int ground = 20;


void render_init(GLFWwindow* window, camera_info *camera){
  window_reference = window;
  glfwMakeContextCurrent(window);
  gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);
  ttf_load_font("./font/ttf/JetBrainsMono-Regular.ttf", 128.0f);
  GLuint vs = compile_shader(GL_VERTEX_SHADER, vertex_shader_source);
  GLuint fs = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_source);
  shader_program = glCreateProgram();
  glAttachShader(shader_program, vs);
  glAttachShader(shader_program, fs);
  glLinkProgram(shader_program);
  glGenVertexArrays(1, &vao);
  glGenBuffers(1, &vbo);
  glBindVertexArray(vao);
  glBindBuffer(GL_ARRAY_BUFFER, vbo);
  glBufferData(GL_ARRAY_BUFFER, sizeof(float) * 12, NULL, GL_DYNAMIC_DRAW);
  glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*) 0);
  glEnableVertexAttribArray(0);
  glClearColor(1, 1, 1, 1);
}

static void draw_rectangle(float x, float y, float w, float h, float r, float g, float b, camera_info* camera, int window_x, int window_y){
  float vertices[12] = {x, y, x+w, y, x+w, y+h, x, y, x+w, y+h, x, y+h};
  glBindBuffer(GL_ARRAY_BUFFER, vbo);
  glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(vertices), vertices);
  glUseProgram(shader_program);
  glUniform3f(glGetUniformLocation(shader_program,"color"), r, g, b);
  glUniform2f(glGetUniformLocation(shader_program,"camera"), (*camera).x, (*camera).y);
  glUniform1f(glGetUniformLocation(shader_program,"zoom"), (*camera).zoom);
  glUniform2f(glGetUniformLocation(shader_program,"window"), window_x, window_y);
  glBindVertexArray(vao);
  glDrawArrays(GL_TRIANGLES, 0, 6);
}

static void draw_triangle(float x1, float y1, float x2, float y2, float x3, float y3, float r, float g, float b, camera_info* camera, int window_x, int window_y){
  float vertices[6] = {x1, y1, x2, y2, x3, y3};
  glBindBuffer(GL_ARRAY_BUFFER, vbo);
  glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(vertices), vertices);
  glUseProgram(shader_program);
  glUniform3f(glGetUniformLocation(shader_program, "color"), r, g, b);
  glUniform2f(glGetUniformLocation(shader_program, "camera"), (*camera).x, (*camera).y);
  glUniform1f(glGetUniformLocation(shader_program, "zoom"), (*camera).zoom);
  glUniform2f(glGetUniformLocation(shader_program, "window"), window_x, window_y);
  glBindVertexArray(vao);
  glDrawArrays(GL_TRIANGLES, 0, 3);
}

static void draw_player(player_info *p, camera_info *camera, int window_x, int window_y){
  draw_rectangle((*p).position.x, (*p).position.y, 16, 16, 1, 0, 0, camera, window_x, window_y);
}

static void draw_ground(int window_x, camera_info *camera, int window_y){
  int first_tile;
  first_tile = (int)((*camera).x / TILE_SIZE) - 1;
  int last_tile;
  last_tile = (int)(((*camera).x + window_x / (*camera).zoom) / TILE_SIZE) + 1;
  for (int i = first_tile; i <= last_tile; i++){
    float world_x;
    world_x = i * TILE_SIZE;
    float world_y;
    world_y = ground * TILE_SIZE;
    draw_rectangle(world_x, world_y, TILE_SIZE, TILE_SIZE, 0.6f, 0.6f, 0.6f, camera, window_x, window_y);
  }
}

void render_menu(void){
  glClear(GL_COLOR_BUFFER_BIT);
  ttf_render_text("PLATFORMER", 1450, 650, 1.0f, 0.5f, 0.5f, 0, 0, 0);
  ttf_render_text("PLAY", 1450, 500, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  ttf_render_text("EDITOR", 1450, 350, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  ttf_render_text("QUIT", 1450, 200, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  switch(main_menu_selected){
    case 0:
       ttf_render_text("->", 1210, 500, 0.9f, 0.5f, 0.5f, 0, 0, 0);
       break;
    case 1:
       ttf_render_text("->", 1210, 350, 0.9f, 0.5f, 0.5f, 0, 0, 0);
       break;
    case 2:
       ttf_render_text("->", 1210, 200, 0.9f, 0.5f, 0.5f, 0, 0, 0);
       break;
  }
}

void render_levels(void){
  glClear(GL_COLOR_BUFFER_BIT);
  ttf_render_text("SELECT LEVEL", 1450, 650, 1.0f, 0.5f, 0.5f, 0, 0, 0);
  int buffer;
  buffer = 500;
  for (int i = 0; i < level_count; i++){
    char level_text[32];
    snprintf(level_text, sizeof(level_text), "LEVEL %d", i + 1);
    ttf_render_text(level_text, 1450, buffer, 0.9f, 0.5f, 0.5f, 0, 0, 0);
    buffer -= 150;
    if (i == level_selected){
      ttf_render_text("->", 1210, buffer + 150, 0.9f, 0.5f, 0.5f, 0, 0, 0);
    }
  }
}

void render_pause(void){
  glClear(GL_COLOR_BUFFER_BIT);
  ttf_render_text("RESUME", 1450, 500, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  ttf_render_text("LEVEL_SELECT", 1459, 350, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  ttf_render_text("MAIN MENU", 1450, 200, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  ttf_render_text("QUIT", 1450, 50, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  switch(pause_selected){
    case 0:
       ttf_render_text("->", 1100, 500, 0.9f, 0.5f, 0.5f, 0, 0, 0);
       break;
    case 1:
       ttf_render_text("->", 1100, 350, 0.9f, 0.5f, 0.5f, 0, 0, 0);
       break;
    case 2:
       ttf_render_text("->", 1100, 200, 0.9f, 0.5f, 0.5f, 0, 0, 0);
       break;
    case 3:
       ttf_render_text("->", 1100, 50, 0.9f, 0.5f, 0.5f, 0, 0, 0);
       break;
  }
}

void render_editor(void){
  glClear(GL_COLOR_BUFFER_BIT);
  ttf_render_text("EDITOR NOT AVAILABLE", 1450, 650, 0.9f, 0.5f, 0.5f, 0, 0, 0);
  ttf_render_text("PRESS ESCAPE", 1450, 500, 0.9f, 0.5f, 0.5f, 0, 0, 0);
}

void render_level_completed(void){
  glClear(GL_COLOR_BUFFER_BIT);
  ttf_render_text("LEVEL COMPLETED!", 1350, 500, 0.9f, 0.5f, 0.5f, 0, 1, 0);
  ttf_render_text("PRESS_ENTER", 1350, 350, 0.9f, 0.5f, 0.5f, 0, 0, 0);
}


void render_update(player_info *p, camera_info* camera, int window_x, int window_y){
  glClear(GL_COLOR_BUFFER_BIT);
  int first_x;
  first_x = (int)((*camera).x / TILE_SIZE) - 1;
  int last_x;
  last_x = (int)(((*camera).x + window_x / (*camera).zoom) / TILE_SIZE) + 1;
  int first_y;
  first_y = 0;
  int last_tile;
  last_tile = max_level_height;
  for (int y = first_y; y < last_tile; y++){
    for (int x = first_x; x < last_x; x++){
      if (x < 0 || x >= max_level_width){
        continue;
      }
      int tile;
      tile = current_level[y][x];
      float world_x;
      float world_y;
      world_x = x * TILE_SIZE;
      world_y = y * TILE_SIZE;
      switch(tile){
        case 1:
           draw_rectangle(world_x, world_y, TILE_SIZE, TILE_SIZE, 0.6f, 0.6f, 0.6f, camera, window_x, window_y);
           break;
        case 2:
           draw_triangle(world_x, world_y + TILE_SIZE, world_x + TILE_SIZE, world_y + TILE_SIZE, world_x + TILE_SIZE / 2, world_y, 1, 0, 0, camera, window_x, window_y);
           break;
        case 3:
           draw_rectangle(world_x, world_y, TILE_SIZE, TILE_SIZE, 0, 1, 0, camera, window_x, window_y);
           break;
      }
    } 
  }
  draw_player(p, camera, window_x, window_y);
}

