#ifndef level_loader_h
#define level_loader_h

extern int max_level_width;
extern int max_level_height;

extern int **current_level;

void load_level(int level_index);
void free_level(void);

#endif
