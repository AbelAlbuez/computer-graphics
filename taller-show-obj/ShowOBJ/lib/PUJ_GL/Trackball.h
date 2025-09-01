// =========================================================================
// @author Abel Albuez Sanchez (aa-albuezs@javeriana.edu.co)
// @author Ricardo Crus (r.cruzs@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Trackball__h__
#define __PUJ_GL__Trackball__h__

#include <Eigen/Core>

namespace PUJ_GL
{
  /**
   * Clase para manejar interacción tipo trackball con el mouse
   */
  class Trackball
  {
  public:
    using TReal = float;
    using TMatrix = Eigen::Matrix< TReal, 4, 4 >;
    using TVector = Eigen::Matrix< TReal, 3, 1 >;

  public:
    Trackball( );
    virtual ~Trackball( );

    // Configurar tamaño de ventana
    void setWindowSize( int width, int height );

    // Obtener matrices de transformación
    const TMatrix& getRotation( ) const;
    TReal getZoom( ) const;
    TReal getPanX( ) const;
    TReal getPanY( ) const;

    // Resetear transformaciones
    void reset( );

    // Manejar eventos del mouse
    void mouseDown( int button, int x, int y );
    void mouseUp( int button );
    bool mouseMove( int x, int y );
    bool mouseWheel( int direction );
    bool mouseDrag( int button, int x, int y );

    // Configurar velocidades
    void setRotationSpeed( TReal speed );
    void setZoomSpeed( TReal speed );
    void setPanSpeed( TReal speed );

  protected:
    // Proyectar punto 2D a esfera unitaria
    TVector projectToSphere( int x, int y );

    // Crear matriz de rotación con fórmula de Rodrigues
    void createRotationMatrix( TMatrix& R, const TVector& axis, TReal angle );

  protected:
    int m_Width;
    int m_Height;
    bool m_MouseDown;
    bool m_Panning;
    int m_LastX;
    int m_LastY;
    int m_ZoomStart;
    TVector m_LastPos;
    TMatrix m_Rotation;
    TReal m_Zoom;
    TReal m_PanX;
    TReal m_PanY;
    TReal m_RotationSpeed;
    TReal m_ZoomSpeed;
    TReal m_PanSpeed;
  };

} // end namespace

#endif // __PUJ_GL__Trackball__h__

// eof - Trackball.h
