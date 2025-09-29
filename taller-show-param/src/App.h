// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================
#ifndef __App__h__
#define __App__h__

#include <PUJ_GL/BaseApp.h>
#include <PUJ_GL/TrackballCamera.h>

/**
 */
class App
  : public PUJ_GL::BaseApp
{
  PUJ_GL_Traits;

public:
  using Self       = App;
  using Superclass = PUJ_GL::BaseApp;

public:
  App(
    int* argc, char** argv,
    int w = 500, int h = 500,
    int x = 10, int y = 10
    );
  virtual ~App( ) override;

  virtual void init( ) override;

protected:
  virtual void _cb_reshape( int width, int height ) override;
  virtual void _cb_display( ) override;
  virtual void _cb_mouse( int button, int state, int x, int y ) override;
  virtual void _cb_special( int key, int x, int y ) override;
  virtual void _cb_keyboard( unsigned char key, int x, int y ) override;

protected:
  void drawBumpMappedPlane(int gridSize, float planeSize, float bumpStrength);
  float sampleImageSmooth(float u, float v);
  float m_bumpStrength = 3.0f;
  int m_gridSize = 100;
  bool m_useSmoothing = true;
  float m_lightAngle = 0.0f;
  

protected:
  PUJ_GL::TrackballCamera m_Camera;
  PUJ_GL::Image* m_Image = nullptr;
};

#endif // __App__h__

// eof - App.h
