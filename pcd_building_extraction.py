import numpy as np
import open3d as o3d
import pcd_division as pcddiv
import pcd_building_ransac as pcdbran

def building_extraction(pcd, row_num, iter_num):
    buildings = []
    for i in range (iter_num):
        row_num = (i+1)*10
        regions = pcddiv.pcd_division(pcd, row_num)
        building_points, other_points = pcdbran.ransac(regions, row_num)
        
        buildings.extend(building_points)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(other_points)

                
    pcd_building = o3d.geometry.PointCloud()
    pcd_building.points = o3d.utility.Vector3dVector(buildings)

    pcd_other = o3d.geometry.PointCloud()
    pcd_other.points = o3d.utility.Vector3dVector(other_points)
    
    return pcd_building