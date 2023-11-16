import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN
import random

def alphamesh(pcd, eps, min_samples, alpha):
    points = np.asarray(pcd.points)

    #Clusterekre bontás
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(points)

    unique_labels = np.unique(labels)

    combined_mesh = o3d.geometry.TriangleMesh()
    pcd_cluster = o3d.geometry.PointCloud()
    
    cl_num = 1

    for label in unique_labels:
        if label == -1:
            continue
        cluster_points = points[labels == label]
            
        pcd_cluster.points = o3d.utility.Vector3dVector(cluster_points)
        
        #Clusterek pontjainak egységes szintbe hozása az épületek formájához
        z_max_height = np.max(cluster_points[:, 2])
        z_min_height = np.min(cluster_points[:, 2])
        
        for point in pcd_cluster.points:
            point[2] = random.uniform(z_max_height, z_min_height-2)

        #Alphamesh alkalmazása az egyes clustereken
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd_cluster, alpha)
        #mesh.compute_vertex_normals()

        combined_mesh += mesh
        print(f'Cluster number {cl_num} is done')
        cl_num += 1

    return combined_mesh
