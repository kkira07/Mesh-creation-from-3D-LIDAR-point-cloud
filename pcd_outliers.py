import open3d as o3d
import numpy as np

def pcd_outliers(pcd, neighbors, std):
    pcd = pcd

    pcd_il, ind_stat = pcd.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=std)
    pcd_ol = pcd.select_by_index(ind_stat, invert=True)
    
    num_removed_points = len(pcd_ol.points)
    print(f"Outlier removal completed, number of removed points: {num_removed_points}")
    
    """"
    pcd_il.paint_uniform_color([0., 1., 0.])
    pcd_ol.paint_uniform_color([1., 0., 0.])
    o3d.visualization.draw_geometries([pcd_il, pcd_ol])
    """
    return pcd_il