import pygame
import moderngl
import sys
from model import *
from camera import Camera
from light import Light

class Engine:
    def __init__(self, win_size=(1280, 720)):
        """Initialize window window with point light source, camera, and cube
        Args:
            win_size (tuple, optional): Window resolution, change to any pixel combination desired, aspect ratio calculations handled. Defaults to (1280, 720).
        """
        pygame.init()
        self.WIN_SIZE = win_size
        # Restrict OpenGL version
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode(self.WIN_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        # Hide mouse pointer, limit mouse from leaving window
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self.context = moderngl.create_context()
        # Change vertex ordering (default set to counter-clock-wise) can change to 'cw' (clock-wise)
        self.context.front_face = 'ccw'
        self.context.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.light = Light()
        self.camera = Camera(self)
        self.scene = Cube(self)
        
    def check_events(self):
        """Determines when the user attempts to close the window
        """
        for event in pygame.event.get():
            # Either they closed out of the window or the ESC key was pressed
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.scene.destroy()
                pygame.quit()
                sys.exit()
                
    def render(self):
        """Renders the scene by calling the render function of the objects, then updating the screen.
        """
        self.context.clear(color = (0.08, 0.16, 0.18))
        self.scene.render()
        pygame.display.flip()
    
    def get_time(self):
        """Gets number of seconds since
        """
        self.time = pygame.time.get_ticks() * 0.001
    
    def run(self):
        """Function that runs the loop for continous rendering
        """
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            #Specify 60FPS runtime, variable stored for camera movement
            self.delta_time = self.clock.tick(60)
    

if __name__ == "__main__":
    app = Engine()
    app.run()