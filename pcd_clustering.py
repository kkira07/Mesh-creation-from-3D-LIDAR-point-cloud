import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN


def clustering(pcd, eps, min_samples):
    points = np.asarray(pcd.points)

    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(points)

    pcd_lamps = o3d.geometry.PointCloud()
    pcd_trees = o3d.geometry.PointCloud()
    pcd_buildings = o3d.geometry.PointCloud()

    unique_labels = np.unique(labels)


    for label in unique_labels:
        if label == -1:
            continue

        cluster_points = points[labels == label]
        
        x_min, x_max = np.min(cluster_points[:, 0]), np.max(cluster_points[:, 0])
        y_min, y_max = np.min(cluster_points[:, 1]), np.max(cluster_points[:, 1])
        z_min, z_max = np.min(cluster_points[:, 2]), np.max(cluster_points[:, 2])
        
        dx = x_max - x_min
        dy = y_max - y_min
        dz = z_max - z_min
        
        #c_color = np.random.rand(3)
        
        if dx < 1.3 and dy < 1.3 and dz > 2:
            lamp_cluster = o3d.geometry.PointCloud()
            lamp_cluster.points = o3d.utility.Vector3dVector(cluster_points)
            #lamp_cluster.paint_uniform_color(c_color)
            pcd_lamps += lamp_cluster
        elif dx < 12 and dx > 1 and dy < 12 and dy > 1 and dz > 3:
            tree_cluster = o3d.geometry.PointCloud()
            tree_cluster.points = o3d.utility.Vector3dVector(cluster_points)
            #tree_cluster.paint_uniform_color(c_color)
            pcd_trees += tree_cluster
        elif (dx > 5 or dy > 5) and dz > 3:
            building_cluster = o3d.geometry.PointCloud()
            building_cluster.points = o3d.utility.Vector3dVector(cluster_points)
            #building_cluster.paint_uniform_color(c_color)
            pcd_buildings += building_cluster
        
    #o3d.visualization.draw_geometries([pcd_buildings, pcd_lamps, pcd_trees])
    return pcd_buildings, pcd_lamps, pcd_trees


