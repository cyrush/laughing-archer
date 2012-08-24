OpenDatabase("noise.silo")
AddPlot("Pseudocolor","hardyglobal")
AddOperator("Isosurface")
iatts = IsosurfaceAttributes()
iatts.contourNLevels = 4
iatts.variable = "default"
SetOperatorOptions(iatts)
DrawPlots()