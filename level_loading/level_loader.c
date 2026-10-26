#include "level_loader.h"
#include <stdio.h>
#include <stdlib.h>

int **current_level;
int max_level_width = 0;
int max_level_height = 0;


void load_level(int level_index){
  char path[64];
  snprintf(path, sizeof(path), "./level%d.map", level_index + 1);
  FILE* level_file;
  level_file = fopen(path, "r");
  if (!level_file){
    fprintf(stderr, "Failed to Open %s\n", path);
    return;
  }
  fscanf(level_file, "%d %d", &max_level_width, &max_level_height);
  current_level = malloc(max_level_height * sizeof(int*));
  for (int y = 0; y < max_level_height; y++){
    current_level[y] = malloc(max_level_width * sizeof(int));
  }
  for (int y = 0; y < max_level_height; y++){
    for (int x = 0; x < max_level_width; x++){
      if (fscanf(level_file, "%d", &current_level[y][x]) != 1){
        current_level[y][x] = 0;
      }
    }
  }
  fclose(level_file);
}

void free_level(void){
  for (int y = 0; y < max_level_height; y++){
    free(current_level[y]);
  }
  free(current_level);
}
