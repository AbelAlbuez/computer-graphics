## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

from .BaseApplication import *
import vtk

"""
"""
class BaseApplicationWithVTK( BaseApplication ):

  '''
  '''
  def __init__( self, title, res_file ):
    super( BaseApplicationWithVTK, self ).__init__( title, res_file )
  # end def

  '''
  '''
  def _parametric_data( self, f, u, v ):
    s = vtk.vtkParametricFunctionSource( )
    s.SetParametricFunction( f )
    s.GenerateNormalsOn( )
    s.GenerateTextureCoordinatesOn( )
    s.SetUResolution( u )
    s.SetVResolution( v )
    s.Update( )

    mesh = s.GetOutput( )
    normals = mesh.GetPointData( ).GetAbstractArray( 'Normals' )
    textures = mesh.GetPointData( ).GetAbstractArray( 'Textures' )

    P = []
    N = []
    T = []
    for i in range( mesh.GetNumberOfPoints( ) ):
      P += [ ( mesh.GetPoint( i ) ) ]
      N += [ ( normals.GetTuple( i ) ) ]
      T += [ ( textures.GetTuple( i ) ) ]
    # end for

    C = []
    for i in range( mesh.GetNumberOfCells( ) ):
      C += [ [] ]
      cell = mesh.GetCell( i )
      for j in range( cell.GetNumberOfPoints( ) ):
        C[ -1 ] += [ cell.GetPointId( j ) ]
      # end for
    # end for

    return ( P, N, T, C )
  # end def

  '''
  '''
  def _sphere( self, r, u = 10, v = 10 ):
    f = vtk.vtkParametricEllipsoid( )
    f.SetXRadius( r )
    f.SetYRadius( r )
    f.SetZRadius( r )
    return self._parametric_data( f, u, v )
  # end def

  '''
  '''
  def _createManualObject( self, data, name, material ):

    P, N, T, C = data

    man = self.m_SceneMgr.createManualObject( name )
    man.begin( material, Ogre.RenderOperation.OT_TRIANGLE_LIST )

    for i in range( len( P ) ):
      man.position( P[ i ] )
      man.normal( N[ i ] )
      man.textureCoord( T[ i ] )
    # end for

    for i in range( len( C ) ):
      if len( C[ i ] ) == 3:
        man.triangle(
            C[ i ][ 0 ], C[ i ][ 1 ], C[ i ][ 2 ]
            )
      elif len( C[ i ] ) == 4:
        man.quad( C[ i ][ 0 ], C[ i ][ 1 ], C[ i ][ 2 ], C[ i ][ 3 ] )
      # end if
    # end for

    man.end( )
    node = self.m_SceneMgr.getRootSceneNode( ).createChildSceneNode( )
    node.attachObject( man )
    return node
  # end def
# end class

## eof - BaseApplicationWithVTK.py
