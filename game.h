#ifndef game_h 
#define game_h

typedef enum{
  game_state_menu,
  game_state_playing,
  game_state_level_select,
  game_state_editor,
  game_state_paused,
  game_state_level_complete,
} game_state;

typedef enum{
  menu_play,
  menu_editor,
  menu_quit,
  menu_count,
} menu_option;

extern int level_count;
extern int main_menu_selected;
extern int level_selected;
extern int pause_selected;
extern bool level_completed;
extern bool levels_completed[100];

#endif 
