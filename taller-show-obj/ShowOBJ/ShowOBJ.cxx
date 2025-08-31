// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// Adaptado con trackball, zoom y pan
// ========================================================================

#include <iostream>
#include <algorithm>
#include <cmath>

#include <Eigen/Core>
#include <PUJ_GL/BaseApp.h>
#include <PUJ_GL/Mesh.h>

/**
 * Visor OBJ con trackball (rotación con botón izquierdo),
 * zoom con rueda y pan con botón medio.
 */
class MyApp : public PUJ_GL::BaseApp
{
public:
  using Self       = MyApp;
  using Superclass = PUJ_GL::BaseApp;

  using TReal   = PUJ_GL::Mesh::TReal;
  using TMatrix = Eigen::Matrix<TReal, 4, 4>;

public:
  MyApp(
    int* argc, char** argv,
    int w = 500, int h = 500,
    int x = 10,  int y = 10
  )
  : Superclass(argc, argv, GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH, w, h, x, y, "Show OBJ models")
  {
    this->m_Camera.setIdentity();
    if(argv != nullptr && argv[1] != nullptr)
      this->m_Mesh.read_from_OBJ(argv[1]);
    else
      std::cerr << "[WARN] use: ./PUJ_GL_ShowOBJ <file.obj>\n";
  }

  virtual ~MyApp() override {}

  virtual void init() override
  {
    this->Superclass::init();
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.05f, 0.05f, 0.07f, 1.0f);
  }

protected:
  // ======= Estado de interacción =======
  // Trackball
  bool m_Dragging { false };
  int  m_LastX { 0 }, m_LastY { 0 };

  // Zoom / Dolly
  TReal m_Dolly { 3.0 };      // distancia cámara-modelo

  // Pan
  bool  m_Panning { false };
  TReal m_PanX { 0 }, m_PanY { 0 };

  // Eje activo para teclado (+/-)
  unsigned char m_Axis { 'y' };

  // ======= Datos de cámara y malla =======
  TMatrix     m_Camera;
  PUJ_GL::Mesh m_Mesh;

  // ======= Utilidad: mapear (x,y) a esfera unitaria =======
  Eigen::Matrix<TReal,4,1> _mapToSphere(int x, int y)
  {
    int w = glutGet(GLUT_WINDOW_WIDTH);
    int h = glutGet(GLUT_WINDOW_HEIGHT);
    TReal nx = (TReal(2)*x - w) / TReal(w);
    TReal ny = (h - TReal(2)*y) / TReal(h);

    TReal len2 = nx*nx + ny*ny;
    TReal z = (len2 <= TReal(1)) ? std::sqrt(TReal(1) - len2) : TReal(0);
    if(len2 > TReal(1)){
      TReal inv = TReal(1) / std::sqrt(len2);
      nx *= inv; ny *= inv;
    }

    Eigen::Matrix<TReal,4,1> v; v << nx, ny, z, TReal(0);
    return v;
  }

  // ======= Callbacks =======
  virtual void _cb_reshape(int width, int height) override
  {
    TReal a = 1.0;
    if(height != 0) a = TReal(width) / TReal(height);

    glViewport(0, 0, width, height);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, a, 0.01, 100.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glutPostRedisplay();
  }

  virtual void _cb_display() override
  {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Cámara: pan + distancia
    glTranslatef(m_PanX, m_PanY, -m_Dolly);

    // Rotaciones acumuladas (teclado + trackball)
    glMultMatrixf(this->m_Camera.data());

    // Ejes
    glBegin(GL_LINES);
      glColor3f(1, 0, 0); glVertex3f(-0.1f, 0, 0); glVertex3f(1, 0, 0);   // X
      glColor3f(0, 1, 0); glVertex3f(0, -0.1f, 0); glVertex3f(0, 1, 0);   // Y
      glColor3f(0, 0, 1); glVertex3f(0, 0, -0.1f); glVertex3f(0, 0, 1);   // Z
    glEnd();

    // Normalización del modelo con su bounding box
    const TReal* bb = this->m_Mesh.bounding_box(); // {xmin,xmax,ymin,ymax,zmin,zmax}
    const TReal cx = (bb[0] + bb[1]) * TReal(0.5);
    const TReal cy = (bb[2] + bb[3]) * TReal(0.5);
    const TReal cz = (bb[4] + bb[5]) * TReal(0.5);
    const TReal sx = (bb[1] - bb[0]);
    const TReal sy = (bb[3] - bb[2]);
    const TReal sz = (bb[5] - bb[4]);
    const TReal maxDim = std::max(sx, std::max(sy, sz));
    const TReal s = (maxDim > TReal(0)) ? (TReal(1.8) / maxDim) : TReal(1);

    glScalef(s, s, s);
    glTranslatef(-cx, -cy, -cz);

    // Dibujo de la malla
    this->m_Mesh.draw();

    glutSwapBuffers();
  }

  virtual void _cb_mouse(int button, int state, int x, int y) override
  {
    // Botón izquierdo: trackball (rotación)
    if(button == GLUT_LEFT_BUTTON){
      if(state == GLUT_DOWN){ m_Dragging = true;  m_LastX = x; m_LastY = y; }
      else if(state == GLUT_UP){ m_Dragging = false; }
    }

    // Botón medio: pan
    if(button == GLUT_MIDDLE_BUTTON){
      if(state == GLUT_DOWN){ m_Panning = true;  m_LastX = x; m_LastY = y; }
      else if(state == GLUT_UP){ m_Panning = false; }
    }

    // Rueda: zoom (freeglut usa 3/4)
    if(state == GLUT_DOWN){
      if(button == 3){ m_Dolly = std::max<TReal>(0.5, m_Dolly - 0.2); glutPostRedisplay(); }
      if(button == 4){ m_Dolly += 0.2;                                 glutPostRedisplay(); }
    }
  }

  virtual void _cb_motion(int x, int y) override
  {
    // Pan activo: mover en X/Y
    if(m_Panning){
      int w = glutGet(GLUT_WINDOW_WIDTH);
      int h = glutGet(GLUT_WINDOW_HEIGHT);
      TReal dx = TReal(x - m_LastX) / TReal(w);
      TReal dy = TReal(y - m_LastY) / TReal(h);

      m_PanX += dx * m_Dolly;   // cuanto más lejos, pan mayor
      m_PanY -= dy * m_Dolly;

      m_LastX = x; m_LastY = y;
      glutPostRedisplay();
      return;
    }

    // Trackball: rotación con botón izquierdo
    if(!m_Dragging) return;

    auto va = _mapToSphere(m_LastX, m_LastY);
    auto vb = _mapToSphere(x, y);

    // eje = va x vb
    Eigen::Matrix<TReal,4,1> axis4;
    axis4 << va(1)*vb(2) - va(2)*vb(1),
             va(2)*vb(0) - va(0)*vb(2),
             va(0)*vb(1) - va(1)*vb(0),
             TReal(0);

    // ángulo = acos(dot(va,vb))
    TReal dot = std::max(TReal(-1), std::min(TReal(1),
                 va(0)*vb(0) + va(1)*vb(1) + va(2)*vb(2)));
    TReal angle = std::acos(dot);

    // Rotación (Rodrigues)
    Eigen::Matrix<TReal,3,1> a = axis4.head<3>();
    TReal n = a.norm();
    if(n < TReal(1e-6)){ m_LastX = x; m_LastY = y; return; }
    a /= n;

    TReal c = std::cos(angle), s = std::sin(angle);
    Eigen::Matrix<TReal,3,3> K;
    K <<    0, -a(2),  a(1),
          a(2),     0, -a(0),
         -a(1),  a(0),    0;
    Eigen::Matrix<TReal,3,3> R3 =
        Eigen::Matrix<TReal,3,3>::Identity()*c
      + (TReal(1)-c)*(a*a.transpose())
      + s*K;

    TMatrix R = TMatrix::Identity();
    R.block<3,3>(0,0) = R3;

    this->m_Camera.transpose() *= R.transpose();

    m_LastX = x; m_LastY = y;
    glutPostRedisplay();
  }

  // Si tu BaseApp usa passive motion, delega aquí
  virtual void _cb_passive_motion(int x, int y) override
  {
    _cb_motion(x, y);
  }

  virtual void _cb_keyboard(unsigned char key, int, int) override
  {
    if( key == 'x' || key == 'X' )      this->m_Axis = 'x';
    else if( key == 'y' || key == 'Y' ) this->m_Axis = 'y';
    else if( key == 'z' || key == 'Z' ) this->m_Axis = 'z';
    else if( key == '+' || key == '-' )
    {
      static const TReal a  = std::atan(TReal(1)) / TReal(45);
      static const TReal ca = std::cos(a);
      static const TReal sa = std::sin(a);

      TMatrix R = TMatrix::Identity();
      if( this->m_Axis == 'x' ){
        R(1,1) = R(2,2) = ca;
        R(1,2) = R(2,1) = sa;
        if(key == '+') R(1,2) *= TReal(-1);
        else           R(2,1) *= TReal(-1);
      }
      else if( this->m_Axis == 'y' ){
        R(0,0) = R(2,2) = ca;
        R(0,2) = R(2,0) = sa;
        if(key == '+') R(2,0) *= TReal(-1);
        else           R(0,2) *= TReal(-1);
      }
      else if( this->m_Axis == 'z' ){
        R(0,0) = R(1,1) = ca;
        R(0,1) = R(1,0) = sa;
        if(key == '+') R(0,1) *= TReal(-1);
        else           R(1,0) *= TReal(-1);
      }
      this->m_Camera.transpose() *= R.transpose();
      glutPostRedisplay();
    }
    else if( key == 'r' || key == 'R' )
    {
      this->m_Camera.setIdentity();
      m_Dolly = 3.0;
      m_PanX = m_PanY = 0;
      m_Dragging = m_Panning = false;
      glutPostRedisplay();
    }
    // Wireframe toggle (opcional):
    else if(key == 'w' || key == 'W')
    {
      static bool wire = true;
      wire = !wire;
      glPolygonMode(GL_FRONT_AND_BACK, wire ? GL_LINE : GL_FILL);
      glutPostRedisplay();
    }
  }
};

// ======= main =======
int main(int argc, char** argv)
{
  MyApp app(&argc, argv);
  app.init();
  app.go();
  return EXIT_SUCCESS;
}
// eof - ShowOBJ.cxx