# PyQt4 imports
from PyQt5 import QtOpenGL, QtWidgets
from PyQt5.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
# Pyhton math lib
from math import pi, cos, sin
import sys

class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 600, 600

    def set_data(self, nodes, edges, config):
        """
        Load 2D data as a Nx2 Numpy array.
        """
        self.nodes  = nodes
        self.edges  = edges
        self.config = config
        self.radius = 0.1

    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)

    def drawGridXY(self):
        """
        Draw grid XY
        """
        gl.glBegin(gl.GL_LINES)
        for i in range(0, self.config.x_max):
            if (i==1):
                gl.glColor3f(.6,.3,.3) 
            else:
                gl.glColor3f(.5,.5,.5)
        
            gl.glVertex2f(i,  self.config.y_min)
            gl.glVertex2f(i, (self.config.y_max-1))
        
            if (i==1):
                gl.glColor3f(.3,.3,.6)
            else:
                gl.glColor3f(.5,.5,.5)

            gl.glVertex2f( self.config.x_min   , i)
            gl.glVertex2f((self.config.x_max-1), i)

        gl.glEnd()

    def drawEdge(self, node1, node2):
        """
        Draw grid XY
        """
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(.2,.6,.3) 

        gl.glVertex2f(node1[0], node1[1])
        gl.glVertex2f(node2[0], node2[1])

        gl.glEnd()

        gl.glLineWidth(20)

    def drawNode(self, x, y, radius):
        """
        Draw filled circle
        """
        i = 0
        triangleAmount = 20 # of triangles used to draw circle
        twicePi = 2.0 * pi
        
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(x, y) # center of circle
        for i in range (i, triangleAmount+1): 
            gl.glVertex2f(  x + (radius * cos(i * twicePi / triangleAmount)), 
                            y + (radius * sin(i * twicePi / triangleAmount)))
        gl.glEnd()

    def paintGL(self):
        """
        Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # draw the grid XY
        self.drawGridXY()
        # draw edges
        for i in range(0, abs(self.config.x_max-self.config.x_min)):
            for j in range(0, abs(self.config.y_max-self.config.y_min)):
                if self.edges[i][j] == 1:
                    self.drawEdge(self.nodes[i], self.nodes[j])
                    print(self.nodes[i], self.nodes[j])
        
        # set yellow color for subsequent drawing rendering calls
        gl.glColor(1,1,0)
        # draw nodes
        for j in range(0, len(self.nodes)):
            self.drawNode(self.nodes[j][0], self.nodes[j][1], self.radius)

    def resizeGL(self, width, height):
        """
        Called upon window resizing: reinitialize the viewport.
        """
        # update the window size
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, width, height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        # gl.glOrtho(-1, 1, 1, -1, -1, 1)
        gl.glOrtho(self.config.x_min, self.config.x_max-1, self.config.y_min, self.config.y_max-1, -1, 1)

# define a Qt window with an OpenGL widget inside it
class TestWindow(QtWidgets.QMainWindow):
    def __init__(self, nodes, edges, config):
        super(TestWindow, self).__init__()
        print (nodes)
        print (edges)
        # initialize the GL widget
        self.widget = GLPlotWidget()
        self.widget.set_data(nodes, edges, config)
        # put the window at the screen position (100, 100)
        self.setGeometry(100, 100, self.widget.width, self.widget.height)
        self.setCentralWidget(self.widget)
        self.show()

def draw_matrix(nodes, edges, config):
    # create the Qt App and window
    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow(nodes, edges, config)
    window.show()
    app.exec_()