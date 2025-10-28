## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import Ogre, Ogre.RTShader
import Ogre.Bites as OgreBites
from .BaseListener import *

"""
"""
class BaseApplication( OgreBites.ApplicationContext ):

  '''
  '''
  m_Listener      = None
  m_ResourcesFile = None
  m_SceneMgr      = None

  '''
  '''
  def __init__( self, title, res_file ):
    super( BaseApplication, self ).__init__( title )
  # end def

  '''
  '''
  def getListener( self ):
    return self.m_Listener
  # end def

  '''
  '''
  def setListener( self, l ):
    self.m_Listener = l
  # end def

  '''
  '''
  def locateResources( self ):
    pass
  # end def

  '''
  '''
  def loadResources( self ):

    self.enableShaderCache( )

    # Load all resources from given locations
    res_mgr = Ogre.ResourceGroupManager.getSingleton( )
    cf = Ogre.ConfigFile( )
    cf.loadDirect( self.m_ResourcesFile )
    settings = cf.getSettingsBySection( )
    for k in settings:
      for i, j in settings[ k ].items( ):
        res_mgr.addResourceLocation( j, i, k )
      # end for
    # end for

    # Initialize all resource groups
    res_mgr.initialiseAllResourceGroups( )

    # Load resources from a specific group
    for k in settings:
      if k != '':
        res_mgr.loadResourceGroup( k )
      # end if
    # end for
  # end def

  '''
  '''
  def setup( self, mgr_type = 'DefaultSceneManager' ):
    super( BaseApplication, self ).setup( )
    self._initSceneManager( mgr_type )
    self.setWindowGrab( True )
    self._loadScene( )
  # end def

  '''
  '''
  def go( self ):
    self.initApp( )
    self.getRoot( ).startRendering( )
    self.closeApp( )
  # end def

  '''
  '''
  def _initSceneManager( self, mgr_type ):
    if self.m_Listener is None:
      self.m_Listener = BaseListener( self.getRoot( ) )
    # end if
    self.addInputListener( self.m_Listener )
    root = self.getRoot( )
    self.m_SceneMgr = root.createSceneManager( mgr_type )
    shadergen = Ogre.RTShader.ShaderGenerator.getSingleton( )
    shadergen.addSceneManager( self.m_SceneMgr )
  # end def

  '''
  '''
  def _loadScene( self ):
    pass
  # end def
# end class

## eof - BaseApplication.py
