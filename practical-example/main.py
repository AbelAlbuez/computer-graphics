import vtk

# Crear una caja (cubo)
box = vtk.vtkBox()
sphere = vtk.vtkSphere()

box.SetBounds(-0.7, 0.7, -0.7, 0.7, -0.7, 0.7)
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.5)

# Combinar las funciones implícitas
f_box_sphere = vtk.vtkImplicitBoolean()
f_box_sphere.AddFunction(sphere)
f_box_sphere.AddFunction(box)
f_box_sphere.SetOperationTypeToIntersection()


c1 = vtk.vtkCylinder()
c2 = vtk.vtkCylinder()
c3 = vtk.vtkCylinder()

c1.SetRadius(0.5)
c2.SetRadius(0.5)
c3.SetRadius(0.5)

c1.SetCenter(0, 0, 0)
c2.SetCenter(0, 0, 0)
c3.SetCenter(0, 0, 0)

c1.SetAxis(0, 0, 1)
c2.SetAxis(1, 0, 0)
c3.SetAxis(0, 1, 0)
f_cyl = vtk.vtkImplicitBoolean()
f_cyl.AddFunction(c1)
f_cyl.AddFunction(c2)
f_cyl.AddFunction(c3)
f_cyl.SetOperationTypeToUnion()

f_final = vtk.vtkImplicitBoolean()
f_final.AddFunction(f_box_sphere)
f_final.AddFunction(f_cyl)
f_final.SetOperationTypeToDifference()

# Muestrear el volumen implícito
sample = vtk.vtkSampleFunction()
sample.SetSampleDimensions(100, 100, 100)
sample.SetImplicitFunction(f_final)
sample.SetModelBounds(-1, 1, -1, 1, -1, 1)

mc = vtk.vtkMarchingCubes()
mc.SetInputConnection(sample.GetOutputPort())
mc.SetValue(0, 0)
mc.Update()

# Configurar el mapeo y renderizado
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(mc.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)


renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.1, 0.1)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(800, 600)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# Iniciar renderizado
renderWindow.Render()
interactor.Start()
