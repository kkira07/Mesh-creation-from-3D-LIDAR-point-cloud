import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN
import random

def alphamesh(pcd, eps, min_samples, alpha):
    points = np.asarray(pcd.points)

    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(points)

    unique_labels = np.unique(labels)

    combined_mesh = o3d.geometry.TriangleMesh()
    pcd_cluster = o3d.geometry.PointCloud()
    
    cl_num = 1
    z_max_threshold = 16
    z_mid_threshold = 10

    for label in unique_labels:
        cluster_points = points[labels == label]
            
        pcd_cluster.points = o3d.utility.Vector3dVector(cluster_points)
            
        for point in pcd_cluster.points:
            z_max_height = random.uniform(10, 25)
            z_mid_height = random.uniform(0, 15)
            z_min_height = random.uniform(-5, 0)
            if point[2] > z_max_threshold: point[2] = z_max_height
            elif point[2] > z_mid_threshold: point[2] = z_mid_height
            else: point[2] = z_min_height

        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd_cluster, alpha)
        mesh.compute_vertex_normals()

        combined_mesh += mesh
        print(f'Cluster number {cl_num} is done')
        cl_num += 1

    return combined_mesh
