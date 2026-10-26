#ifndef text_render_h
#define text_render_h

#include <glad/glad.h>

void ttf_load_font(const char* path, float pixel_height);

void ttf_render_text(const char* text, float x, float y, float scale, float anchor_x, float anchor_y, float r, float g, float b);

void ttf_free_font(void);

#endif
