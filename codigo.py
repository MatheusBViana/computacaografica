import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

#Global
scale = 0.01
change_scale = 1.0
TAM = 0.1
TAM3 = 0.05
t_x =  0.0
t_y = 0.0
p_x =  0.0 
p_y = 0.0
s =  2.0
angle = 0.0
angle2 = 0.0
dia = 1
noite = 0

def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

#Key Event
def key_event(window,key,scancode,action,mods):
    global p_x, p_y, s, angle2, change_scale
    
    if (key == 68 and p_x <  0.7): p_x += 0.01 # D
    if(key == 65 and p_x > -0.7): p_x -= 0.01 # A

    if(key == 87 and p_y <  0.4): p_y += 0.01 # W
    if(key == 83 and p_y > -0.2): p_y -= 0.01 # S

    if(key == 265 ): change_scale += 0.1 # UP arrow
    if(key == 264 ): change_scale -= 0.1 # Down arrow  

    if(key == 262): angle2 += 0.02 # Right arrow
    if(key == 263): angle2 -= 0.02 # Left arrow

# Entrada: angulo de longitude, latitude, raio
# Saida: coordenadas na esfera
def F(u,v,r):
    x_lua = r*math.sin(v)*math.cos(u)
    y = r*math.sin(v)*math.sin(u)
    z = r*math.cos(v)
    return (x_lua,y,z)

#Vértices para a estrela
#Entrada: Vetor de vértices
def desenha_sol(vertices):
    vertices['position'][0] = [0.0, 0.0]

    step = np.pi/8
    ang = 0.0

    for i in range(17):
        if(i % 2 == 1):
            vertices['position'][i] = [0.6 * TAM * np.cos(ang),0.6 * TAM * np.sin(ang)]
        else:
            vertices['position'][i] = [0.55 * TAM * np.cos(ang), 0.55 * TAM * np.sin(ang)]

        ang += step
    
    vertices['position'][17] = vertices['position'][1]

#Vértices para a Flor 1
#Entrada: Vetor de vértices
def drawFlower1(vertices):
    step = np.pi/6
    ang = 0.0

    #Pétalas
    for i in range(18,66,4):
        smallstep = step/7

        vertices['position'][i] = [0.0,0.0]

        vertices['position'][i+1] = [0.7 * TAM * np.cos(ang + 2 * smallstep),0.7 * TAM * np.sin(ang + 2 * smallstep)]

        vertices['position'][i+2] = [1.0 * TAM * np.cos(ang + 4 * smallstep),1.0 * TAM * np.sin(ang + 4 * smallstep)]

        vertices['position'][i+3] = [0.7 * TAM * np.cos(ang + 6 * smallstep),0.7 * TAM * np.sin(ang + 6 * smallstep)]    

        ang += step

    #Cabo
    vertices['position'][66] = [0.002,0]

    vertices['position'][67] = [-0.002,0]

    vertices['position'][68] = [-0.002,-0.3]
    
    vertices['position'][69] = [+0.002,-0.3]

#Vértices para a Flor 2
#Entrada: Vetor de vértices
def drawFlower2(vertices):
    step = np.pi/4
    ang = 0.0

    #Pétalas
    for i in range(70,118,4):
        smallstep = step/7

        vertices['position'][i] = [0.0,0.0]

        vertices['position'][i+1] = [-0.7 * TAM * np.cos(ang + 2 * smallstep),0.7 * TAM * np.sin(ang + 2 * smallstep)]

        vertices['position'][i+2] = [-1.0 * TAM * np.cos(ang + 4 * smallstep),1.0 * TAM * np.sin(ang + 4 * smallstep)]

        vertices['position'][i+3] = [-0.7 * TAM * np.cos(ang + 6 * smallstep),0.7 * TAM * np.sin(ang + 6 * smallstep)]    

        ang += step

    #Cabo
    vertices['position'][118] = [-0.002,0.0]

    vertices['position'][119] = [0.002,0.0]

    vertices['position'][120] = [0.002,-0.3]
    
    vertices['position'][121] = [-0.002,-0.3]

#Vértices para o Homem
#Entrada: Vetor de vértices
def drawMan(vertices):
    ang = 0
    radius = 0.2
    ax_move = -0.0
    ay_move = 0.0

    #Corpo
    vertices['position'][122] = [0.0,0.0]
    
    vertices['position'][123] = [0.0,-0.15]
    vertices['position'][124] = [0.1,-0.2]
    vertices['position'][125] = [0.0,-0.15]
    vertices['position'][126] = [-0.1,-0.2]
    vertices['position'][127] = [0.0,-0.15]
    vertices['position'][128] = [0.0,-0.3]
    vertices['position'][129] = [-0.05,-0.45]
    vertices['position'][130] = [0.0,-0.3]
    vertices['position'][131] = [0.05,-0.45]
    vertices['position'][133] = [0.0,-0.3]
    
    #Cabeça
    vertices['position'][133] = [0.0,0.0]
    for i in range(134,165):
	    ang += (2.0*np.pi)/30
	    vertices['position'][i] = [0.4*np.cos(ang)*radius+ax_move,0.4*np.sin(ang)*radius+ay_move]
    
    
#Vértices para a Árvore
#Entrada: Vetor de vértices
def drawTree(vertices):
    vertices['position'][165] = [0.0,0.0]
    #Copa
    vertices['position'][166] = [0.05,0.0]
    vertices['position'][167] = [0.0,0.9]
    vertices['position'][168] = [-0.05,0.0]

    #Folhas 1
    vertices['position'][169] = [0.5,0.5]
    vertices['position'][170] = [0.0,1.1]
    vertices['position'][171] = [-0.5,0.5]

    vertices['position'][172] = [0.5, .9]
    vertices['position'][173] = [0.0, 0.3]
    vertices['position'][174] = [-0.5, .9]

def desenha_lua(vertices):
    vertices['position'][175] = [0.0, 0.0]

    step = np.pi/8
    ang = 0.0

    for i in range(176,193):
        if(i % 2 == 1):
            vertices['position'][i] = [0.65 * TAM * np.cos(ang),0.65 * TAM * np.sin(ang)]
        else:
            vertices['position'][i] = [0.65 * TAM * np.cos(ang), 0.65 * TAM * np.sin(ang)]

        ang += step
    
    vertices['position'][193] = vertices['position'][1]


def main():
    global angle, angle2
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(1000, 800, "Trabalho 1", None, None)
    glfw.make_context_current(window)

    vertex_code = """
            attribute vec3 position;
            uniform mat4 mat_transformation;
            void main(){
                gl_Position = mat_transformation * vec4(position,1.0);
            }
            """
    fragment_code = """
            uniform vec4 color;
            void main(){
                gl_FragColor = color;
            }
            """

    # Request a program and shader slots from GPU
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # Set shaders source
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # Compile shaders
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Vertex Shader")

    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Fragment Shader")

    # Attach shader objects to the program
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    # Build program
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    # Make program the default program
    glUseProgram(program)

    # Prepare 3 coordinates for 2 slot vector
    vertices = np.zeros(250, [("position", np.float32, 2)])

    desenha_sol(vertices)      #Star
    drawFlower1(vertices)   #Flower 1
    drawFlower2(vertices)   #Flower 2
    drawMan(vertices)       #Man
    drawTree(vertices)      #Tree
    desenha_lua(vertices) #
    

    # Request a buffer slot from GPU
    buffer = glGenBuffers(1)
    # Make this buffer the default one
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # Upload data
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # Bind the position attribute
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)

    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

    loc_color = glGetUniformLocation(program, "color")
    R = 1.0
    G = 0.0
    B = 0.0

    glfw.set_key_callback(window,key_event)

    glfw.show_window(window)

    x = 0.0
    x_lua = -1.2
    step = np.pi/900
    mult = 1.0
    angle = 0.0
    dia = 1
    noite = 0
    
    vermelho = 1
    verde = 0.7
    azul = 0.7

    while not glfw.window_should_close(window):

        glfw.poll_events() 

        
        glClear(GL_COLOR_BUFFER_BIT) 
        glClearColor(vermelho, verde, azul, 1.0)
        # glClearColor(.1, .1, .1, .1)
        # if (dia == 0):
        #     vermelho -= 0.00015
        #     verde -= 0.00015
        #     azul -= 0.00015
        if (dia == 1):
            if(x < 0.1):
                vermelho += 0.00015
                verde += 0.0001
                azul += 0.00001
            else:
                vermelho -= 0.0003
                verde -= 0.00015
                azul -= 0.0001



        loc = glGetUniformLocation(program, "mat_transformation");

        mat_aux = np.zeros(16)
        mat_final = np.zeros(16)

        #### STAR ####
        t_x = x
        # t_y = mult * 0.1 * np.sin(4*x) # Faz o caminho da senoide
        
        if(np.fabs(t_y) < 0.001 and np.fabs(x) > 0.001):
            step *= (-1)
            mult *= (-1)
        

        if (dia == 1):
            x += 0.00071
            
            if x >= 1.2:
                x = -1.3
                vermelho = 0.1
                verde = 0.1
                azul = 0.1
                dia = 0

        # Matrix: Scale
        mat_scale = np.array([
            s   , 0.0, 0.0, 0.0,
            0.0,    s, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])
        
        # Matrix: Rotation
        mat_rotation = np.array([
            np.cos(angle), -np.sin(angle), 0.0, 0.0,
            np.sin(angle),  np.cos(angle), 0.0, 0.0,
            0.0      ,  0.0      , 1.0, 0.0,
            0.0      ,  0.0      , 0.0, 1.0
        ])

        # Matrix: Translation
        mat_translation = np.array([
            1.0, 0.0, 0.0, t_x ,
            0.0, 1.0, 0.0, t_y + 0.7,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])

        # Multiplex Matrix
        mat_aux = multiplica_matriz(mat_scale, mat_scale)
        mat_final = multiplica_matriz(mat_translation, mat_aux)

        # Continuos star rotation
        angle -= 0.005

        #Send transformation matrix
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_final)

	    #Color Render
        glUniform4f(loc_color, 254.0/255.0, 254.0/255.0, 68.0/255.0, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 18)

        #### FLOWER 1 ####
        
        # Alterando a matriz de translação para a flor 1
        mat_translation[3] = p_x-0.1
        mat_translation[7] = p_y+0.05

        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)

        # Cabo da flor
        glUniform4f(loc_color, 0.0, 128.0/255.0, 0.0/255.0, 1.0) # Cor verde
        glDrawArrays(GL_LINE_STRIP, 66, 4)

        # Alterando as matrizes de rotação e escala para a flor 1
        mat_scale[0] = 1.0
        mat_scale[5] = 1.0

        mat_rotation[0] =  np.cos(angle2)
        mat_rotation[1] = -np.sin(angle2)
        mat_rotation[4] =  np.sin(angle2)
        mat_rotation[5] =  np.cos(angle2)        
        
        mat_aux = multiplica_matriz(mat_rotation, mat_scale)
        mat_final = multiplica_matriz(mat_translation, mat_aux)

        # enviando a matriz de transformacao para a GPU, vertex shader, variavel mat_transformation
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_final)
    
        glUniform4f(loc_color, 150.0/255.0, 0.0, 205.0/255.0, 1.0)# Cor roxa
        
        #Pétalas
        for j in range(0,12):
            glDrawArrays(GL_TRIANGLE_FAN, 18 + 4*j, 4)

        #### FLOWER 2 ####

        # Alterando a matriz de translação para a flor 2
        mat_translation[3] = 0.6
        mat_translation[7] = -0.65

        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)

        # Cabo da flor
        glUniform4f(loc_color, 0.0, 128.0/255.0, 0.0/255.0, 1.0) # Cor verde
        glDrawArrays(GL_LINE_STRIP, 118, 4)

        # Alterando as matrizes de rotação e escala para a flor 2
        mat_scale[0] = 1.5
        mat_scale[5] = 1.5

        mat_rotation[0] =  np.cos(-angle2)
        mat_rotation[1] =  -np.sin(-angle2)
        mat_rotation[4] =  np.sin(-angle2)
        mat_rotation[5] =  np.cos(-angle2)        
        
        mat_aux = multiplica_matriz(mat_rotation, mat_scale)
        mat_final = multiplica_matriz(mat_translation, mat_aux)

        # enviando a matriz de transformacao para a GPU, vertex shader, variavel mat_transformation
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_final)
    
        glUniform4f(loc_color, 1.0, 0.0, 0.0, 1.0)# Cor Vermelha
        
        for j in range(0,12):
            glDrawArrays(GL_TRIANGLE_FAN, 70 + 4*j, 4)                



        #### ARVORE  #####

        # Alterando a matriz de translação para a árvore
        mat_translation[3] = 0.5
        mat_translation[7] = -0.3  
        mat_scale[0] =  0.5
        mat_scale[5] =  0.85    

        mat_rotation[0] =  np.cos(-angle2)
        mat_rotation[1] =  -np.sin(-angle2)
        mat_rotation[4] =  np.sin(-angle2)
        mat_rotation[5] =  np.cos(-angle2)  
        mat_final = multiplica_matriz(mat_translation, mat_scale)
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_final)


        # Alterando a matriz de translação para a árvore
        mat_translation[3] = -0.6
        mat_translation[7] = -0.2  
        mat_scale[0] =  0.5
        mat_scale[5] =  change_scale*0.5    
        mat_final = multiplica_matriz(mat_translation, mat_scale)

        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_final)

	    #renderizando
        glUniform4f(loc_color,190/110, 20/250, 190/255, 1.0) #Cor Marrom
        glDrawArrays(GL_TRIANGLE_FAN, 166, 3)
        glUniform4f(loc_color, 255, 0, 255, 1.0) #Cor Verde
        glDrawArrays(GL_TRIANGLE_FAN, 169, 3)
        glDrawArrays(GL_TRIANGLE_FAN, 172, 3)

        #### Homem ####

        # Alterando a matriz de translação para o homem
        mat_translation[3] = p_x
        mat_translation[7] = p_y        

        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)
        
        #renderizando
        glUniform4f(loc_color, 0, 0.5, 1, 1.0) #Cor Preta
        glLineWidth(4.0)
        glDrawArrays(GL_LINE_STRIP, 122, 10)
        glDrawArrays(GL_TRIANGLE_FAN, 134, 31)    

        #### LUA ####
        
        t_x = x_lua
        # t_y = mult * 0.1 * np.sin(4*x_lua) # Faz o caminho da senoide
        
        # if(np.fabs(t_y) < 0.001 and np.fabs(x_lua) > 0.001):
        #     step *= (-1)
        #     mult *= (-1)
        if (dia == 0):
            x_lua += 0.00051
            if x_lua >= 1.2:
                dia = 1
                x_lua = -1.2

        # Matrix: Scale
        mat_scale = np.array([
            s   , 0.0, 0.0, 0.0,
            0.0,    s, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])
        
        # Matrix: Rotation
        mat_rotation = np.array([
            np.cos(angle), -np.sin(angle), 0.0, 0.0,
            np.sin(angle),  np.cos(angle), 0.0, 0.0,
            0.0      ,  0.0      , 1.0, 0.0,
            0.0      ,  0.0      , 0.0, 1.0
        ])

        # Matrix: Translation
        mat_translation = np.array([
            1.0, 0.0, 0.0, t_x ,
            0.0, 1.0, 0.0, t_y + 0.7,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ])

        # Multiplex Matrix
        mat_lua = mat_scale
        mat_final = multiplica_matriz(mat_translation, mat_lua)

        # Continuos star rotation
        angle -= 0.005

        #Send transformation matrix
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_final)

	    #Color Render
        glUniform4f(loc_color, 255, 255, 255, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 175, 193)

	     

        glfw.swap_buffers(window)

    glfw.terminate()

#Função MAIN
if __name__ == "__main__":
  main()
