DeleteAllPlots()
OpenDatabase("noise.silo")
AddPlot("Pseudocolor","radial")
AddOperator("Isosurface")
iatts = IsosurfaceAttributes()
iatts.contourNLevels = 4
iatts.variable = "hardyglobal"
SetOperatorOptions(iatts)
DrawPlots()