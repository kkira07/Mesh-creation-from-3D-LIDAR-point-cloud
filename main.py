import numpy as np
import open3d as o3d
import pyvista as pv
import pcd_outliers as pcdol
import pcd_division as pcddiv
import pcd_ransac as pcdran
import pcd_above_ground_cleaning as pcdagc
import pcd_building_extraction as pcdbe
import pcd_clustering as pcdcl
import mesh_alphashapes as mesha
import mesh_placing as meshp
import mesh_delaunay as meshd

pcd = o3d.io.read_point_cloud("final/resources/campus_whole.ply")
pcd.paint_uniform_color([1., 1., 1.])

#Kívülálló pontok eltávolítása kismértékben
neighbors = 5
std = 10.0
pcd =pcdol.pcd_outliers(pcd, neighbors, std)

#A földi és föld feletti pontok elválasztása RANSAC algoritmussal
#Nem szükséges a paramétereken módosítani más pontfelhő esetében sem
fine_tune_iter = 4 #finomhangolási iterációk száma
iter_num = 1000 #RANSAC iterációszám
max_threshold = 0.5 #RANSAC maximális és minimális hibahatára
min_threshold = 0.3
remaining_points = []
for i in range(fine_tune_iter):
    row_number = (i*50)+100
    if i == fine_tune_iter-1: #Utolsó iteráció paraméterei
        threshold = 1
        row_number = 4
    elif i == fine_tune_iter-2: threshold = min_threshold #Utolsó előtti iteráció paraméterei
    else: threshold = max_threshold-(i*(max_threshold/fine_tune_iter))
    
    if i > 0 and i < fine_tune_iter*0.25: iter_num = 100
    elif i >= fine_tune_iter*0.25: iter_num = 20
    
    regions = pcddiv.pcd_division(pcd, row_number) #Pontfelhő felosztása régiókra az xy síkon
    
    ground_points, above_ground_points = pcdran.ransac(regions, row_number, threshold, iter_num) #RANSAC algoritmus az egyes régiókon
    
    remaining_points.extend(above_ground_points) #Föld feletti pontként azonosított objektumok listájának kiterjesztése
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(ground_points)
    print(f"RANSAC iteration {i+1} of {fine_tune_iter} is complete")
    print(f"Number of current regions: {row_number*row_number}, current iteration number: {iter_num}")

pcd_agr = o3d.geometry.PointCloud()
pcd_agr.points = o3d.utility.Vector3dVector(remaining_points)
"""
pcd.paint_uniform_color([0., 0., 1.])
pcd_agr.paint_uniform_color([0., 0., 0.])
o3d.visualization.draw_geometries([pcd, pcd_agr])
"""
o3d.io.write_point_cloud("final/output/ground_points_temp.ply", pcd) #Földi pontok fájlba írása és memóriából való törlése, amíg szükség nem lesz rájuk

del pcd

print("RANSAC complete")

#Föld feletti pontok tisztítása
row_number = 800
z_max = -100
z_min = 100
outliers = []
inliers = []

regions = pcddiv.pcd_division(pcd_agr, row_number)
pcd = pcdagc.cleaning(regions, row_number, z_max, z_min)
"""
pcd_agr.paint_uniform_color([1., 0., 0.])
pcd.paint_uniform_color([0., 1., 0.])
o3d.visualization.draw_geometries([pcd_agr, pcd])
"""
del pcd_agr
print("Cleaning of the cloud complete")

#Pontok számának csökkentése
num_points_to_keep = 1000000

if len(pcd.points) > num_points_to_keep:
    indices = np.random.choice(len(pcd.points), num_points_to_keep, replace=False)
    pcd = pcd.select_by_index(indices)
    
print(f'Point count reduced to {num_points_to_keep}')


#Föld feletti pontok további tisztítása
row_number = 100
iter_num = 5
pcd = pcdbe.building_extraction(pcd, row_number, iter_num)

print("Second phase of cleaning complete")

#Föld feletti pontok szétválasztása épületekre, fákra, villanyoszlopokra és beazonosíthatatlan objektumokra
eps = 1.7
min_samples = 50
pcd, pcd_lamps, pcd_trees = pcdcl.clustering(pcd, eps, min_samples)
o3d.io.write_point_cloud("final/output/tree_points_temp.ply", pcd_trees)
o3d.io.write_point_cloud("final/output/lamp_points_temp.ply", pcd_lamps)
del pcd_trees, pcd_lamps
print("Separation complete")

#Épületek modellé alakítása
eps = 2
min_samples = 20
alpha = 200
mesh = mesha.alphamesh(pcd, eps, min_samples, alpha)
o3d.io.write_triangle_mesh("final/output/buildings_temp.obj", mesh)
del pcd, mesh
print("Mesh creation from buildings complete")

#Fák és lámpák elhelyezése
pcd_trees = o3d.io.read_point_cloud("final/output/tree_points_temp.ply")
tree_dummy = o3d.io.read_triangle_mesh("final/resources/tree.obj")
pcd_lamps = o3d.io.read_point_cloud("final/output/lamp_points_temp.ply")
lamp_dummy = o3d.io.read_triangle_mesh("final/resources/lamp.obj")
eps = 1.5
min_samples = 50
mesh_trees = meshp.dummy_placing(pcd_trees, tree_dummy, eps, min_samples)
mesh_lamps = meshp.dummy_placing(pcd_lamps, lamp_dummy, eps, min_samples)
o3d.io.write_triangle_mesh("final/output/lamps_temp.obj", mesh_lamps)
o3d.io.write_triangle_mesh("final/output/trees_temp.obj", mesh_trees)
del pcd_trees, pcd_lamps, tree_dummy, lamp_dummy, mesh_trees, mesh_lamps
print("Trees and streetlamps added")

#Földi pontok modellé alakítása
pcd_ground = o3d.io.read_point_cloud("final/output/ground_points_temp.ply")
num_points_to_keep = 3000000
mesh_ground = meshd.delaunay_ground(pcd_ground, num_points_to_keep)
print("Ground complete")

#Teljes modell összerakása
mesh_buildings = o3d.io.read_triangle_mesh("final/output/buildings_temp.obj")
mesh_trees = o3d.io.read_triangle_mesh("final/output/trees_temp.obj")
mesh_lamps = o3d.io.read_triangle_mesh("final/output/lamps_temp.obj")
combined_mesh = mesh_lamps + mesh_trees + mesh_ground + mesh_buildings
o3d.io.write_triangle_mesh("final/output/full_mesh.obj", combined_mesh)


o3d.visualization.draw_geometries([combined_mesh])

