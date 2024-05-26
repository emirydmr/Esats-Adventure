from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(WINDOW)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("testest")
        map_path = join("..","data","levels","omni.tmx")
        self.tmx_map = {0: load_pygame(map_path)}
        self.assets()

        self.current_stage = Level(self.tmx_map[0],self.esat_frames)
    def assets(self):
        self.esat_frames = {"player": import_sub_folders("..","assets","Esat","sprites")}
    def run(self):
        while True:
            dt = self.clock.tick(TICKSPEED) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_stage.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game_instance = Game()
    game_instance.run()
    print(self.esat_frames)
