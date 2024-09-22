import glm
import pygame

# Camera global variables
FOV = 80
NEAR = 0.1
FAR = 100
# Speed sensitivty for spatial movement
SPEED = 0.01
# Mouse sensitivty for perspective movement
SENSITIVITY = 0.05

class Camera:
    def __init__(self, app, position=(0,0,4), yaw=-90, pitch=0):
        """Initializes a camera object

        Args:
            app (Engine()): Passes parent engine object for access to other objects in scene
            position (tuple, optional): Defines position of camera. Defaults to (0,0,4).
            yaw (int, optional): Initial yaw angle. Defaults to -90.
            pitch (int, optional): Initial pitch angle. Defaults to 0.
        """
        self.app = app
        # Determine aspect ratio of window
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        # Unit vectors for movement
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0,0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # View matrix
        self.m_view = self.get_view_matrix()
        # Projection matrix
        self.m_proj = self.get_projection_matrix()
        
    def rotate(self):
        """Rotate camera based off mouse movement and sensitivity
        """
        rel_x, rel_y = pygame.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))
    
    def update_camera_vectors(self):
        """Update camera vectors based off change in yaw and pitch
        """
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)
        
        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))
        
    def update(self):
        """Called during every frame to update based off movement
        """
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()
        
    def move(self):
        """Moves camera based off key presses. WASD + QE for vertical mobility
        """
        velocity = SPEED * self.app.delta_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position += self.forward * velocity
        if keys[pygame.K_s]:
            self.position -= self.forward * velocity
        if keys[pygame.K_a]:
            self.position -= self.right * velocity
        if keys[pygame.K_d]:
            self.position += self.right * velocity
        if keys[pygame.K_q]:
            self.position += self.up * velocity
        if keys[pygame.K_e]:
            self.position -= self.up * velocity
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)
        
    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

    