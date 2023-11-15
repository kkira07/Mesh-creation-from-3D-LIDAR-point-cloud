import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN

def dummy_placing(pcd, mesh, eps, min_samples):
    points = np.asarray(pcd.points)

    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(points)

    unique_labels = np.unique(labels)

    combined_mesh = o3d.geometry.TriangleMesh()
    pcd_cluster = o3d.geometry.PointCloud()

    lowest_all = 0
    cluster_num = 0

    for label in unique_labels:
        cluster_points = points[labels == label]
        lowest_point = min(cluster_points, key=lambda p: p[2])
        lowest_all += lowest_point[2]
        cluster_num += 1

    avg_lowest = lowest_all/cluster_num

    for label in unique_labels:
        cluster_points = points[labels == label]
            
        pcd_cluster.points = o3d.utility.Vector3dVector(cluster_points)
        
        lowest_point = min(cluster_points, key=lambda p: p[2])

        model = o3d.geometry.TriangleMesh()
        model.vertices = o3d.utility.Vector3dVector(np.asarray(mesh.vertices))
        model.triangles = o3d.utility.Vector3iVector(np.asarray(mesh.triangles))

        if lowest_point[2] < (avg_lowest+5): model.translate(lowest_point)

        combined_mesh += model

    return combined_mesh
