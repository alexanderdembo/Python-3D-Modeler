import numpy
import glm
import pygame

class Cube:
    def __init__(self, app):
        self.app = app
        self.context = app.context
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='textures/img.png')
        self.on_init()
    
    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.context.texture(size=texture.get_size(), components=3,
                                       data=pygame.image.tostring(texture, 'RGB' ))
        return texture
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time * 0.5, glm.vec3(0, 1, 0))
        self.shader_program['m_model'].write(m_model)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['camPos'].write(self.app.camera.position)
    
    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model
    
    def on_init(self):
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.Id'].write(self.app.light.Id)
        self.shader_program['light.Is'].write(self.app.light.Is)
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)
    
    def render(self):
        self.update()
        self.vao.render()
        
    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        
    def get_vao(self):
        vao = self.context.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f', 'in_texcoord_0', 'in_normal', 'in_position')])
        return vao
    
    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2), (1, 7, 2), (1, 6, 7), 
                   (6, 5, 4), (4, 7, 6), (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7), (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        
        texture_coordinates = [(0,0), (1, 0), (1, 1), (0, 1)]
        texture_coordinate_indices = [(0, 2, 3), (0, 1, 2), (0, 2, 3), (0, 1, 2), (0, 1, 2), (2, 3, 0), (2, 3, 0), (2, 0, 1), (0, 2, 3), (0, 1, 2), (3, 1, 2), (3, 0, 1),]
        texture_coordinate_data = self.get_data(texture_coordinates, texture_coordinate_indices)
        
        normals = [(0,0, 1) * 6, (1, 0, 0) * 6, (0, 0, -1) * 6, (-1, 0, 0) * 6, (0, 1, 0) * 6, (0, -1, 0) * 6]
        
        normals = numpy.array(normals, dtype='f4').reshape(36, 3)
        
        vertex_data = numpy.hstack([normals, vertex_data])
        vertex_data = numpy.hstack([texture_coordinate_data, vertex_data])
        
        return vertex_data
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='f4')
    
    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.context.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.context.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)
        return program