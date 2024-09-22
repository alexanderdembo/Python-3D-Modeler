import glm

class Light:
    def __init__(self, position=(3, 3, -3), color=(1, 1, 1)):
        """Define our light source

        Args:
            position (tuple, optional): Position of light source. Defaults to (3, 3, -3).
            color (tuple, optional): Color of light. Defaults to (1, 1, 1) (White).
        """
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        # Phong lighting ambient, diffuse, and specular light ratios
        self.Ia = 0.1 * self.color
        self.Id = 0.8 * self.color
        self.Is = 1.0 * self.color