## -------------------------------------------------------------------------
## @author Abel (Taller 4 - Ogre3D FPS)
## GeometryFactory - Generador de geometrías con VTK
## -------------------------------------------------------------------------

import vtk
import Ogre

class GeometryFactory:
    
    @staticmethod
    def create_sphere(scene_mgr, name, radius, material_name):
        """Crea una esfera usando VTK"""
        vsphere = vtk.vtkSphereSource()
        vsphere.SetRadius(radius)
        vsphere.SetThetaResolution(30)  # Resolución horizontal
        vsphere.SetPhiResolution(30)    # Resolución vertical
        vsphere.Update()
        
        return GeometryFactory._vtk_to_ogre(
            scene_mgr, name, vsphere.GetOutput(), material_name
        )
    # end def
    
    @staticmethod
    def create_cylinder(scene_mgr, name, radius, height, material_name):
        """Crea un cilindro usando VTK"""
        vcylinder = vtk.vtkCylinderSource()
        vcylinder.SetRadius(radius)
        vcylinder.SetHeight(height)
        vcylinder.SetResolution(30)
        vcylinder.Update()
        
        return GeometryFactory._vtk_to_ogre(
            scene_mgr, name, vcylinder.GetOutput(), material_name
        )
    # end def
    
    @staticmethod
    def _vtk_to_ogre(scene_mgr, name, vtk_output, material_name):
        """Convierte VTK PolyData a Ogre ManualObject"""
        man = scene_mgr.createManualObject(name)
        man.begin(material_name, Ogre.RenderOperation.OT_TRIANGLE_LIST)
        
        # Transferir vértices
        for i in range(vtk_output.GetNumberOfPoints()):
            pos = vtk_output.GetPoint(i)
            man.position(pos)
        # end for
        
        # Transferir triángulos
        for i in range(vtk_output.GetNumberOfCells()):
            cell = vtk_output.GetCell(i)
            if cell.GetNumberOfPoints() == 3:
                man.triangle(
                    cell.GetPointId(0),
                    cell.GetPointId(1),
                    cell.GetPointId(2)
                )
            # end if
        # end for
        
        man.end()
        return man
    # end def

# end class

## eof - GeometryFactory.py