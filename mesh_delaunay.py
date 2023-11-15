import pyvista as pv
import numpy as np
import open3d as o3d


def delaunay_ground(pcd, num_points_to_keep):
    if len(pcd.points) > num_points_to_keep:
        indices = np.random.choice(len(pcd.points), num_points_to_keep, replace=False)
        pcd = pcd.select_by_index(indices)

    points = np.asarray(pcd.points)
    cloud = pv.PolyData(points)
    
    #Delaunay-trianguláció
    triangulated_mesh = cloud.delaunay_2d()

    pl = pv.Plotter()
    _ = pl.add_mesh(triangulated_mesh)
    #Fájlba írás az Open3D konverzióhoz
    pl.export_obj("final/output/mesh_ground_temp.obj")

    mesh_ground = o3d.io.read_triangle_mesh("final/output/mesh_ground_temp.obj")
    #Mesh felbontásának csökkentése
    mesh_smp = mesh_ground.simplify_quadric_decimation(target_number_of_triangles=2000000)

    #Kiutgó csúcsok csökkentése
    mesh = mesh_smp.filter_smooth_laplacian(10, 0.5) 
    return mesh
