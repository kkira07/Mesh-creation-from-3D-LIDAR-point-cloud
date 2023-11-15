import numpy as np
import open3d as o3d


def ransac(regions, row_number):
    building_points = []
    other_points = []
    normal_vector_horizontal = np.array([0, 0, 1])
    for row in range(row_number):
        for col in range(row_number):
            region_points = np.asarray(regions[row][col])
            if len(region_points) < 3: continue 
            region_pcd = o3d.geometry.PointCloud()
            region_pcd.points = o3d.utility.Vector3dVector(region_points)

            plane_model, inliers = region_pcd.segment_plane(
                distance_threshold=0.2, ransac_n=3, num_iterations=300
            )
            normal_vector = np.array(plane_model[:-1])
            dot_product = np.dot(normal_vector_horizontal, normal_vector)
            magnitude_horizontal = np.linalg.norm(normal_vector_horizontal)
            magnitude = np.linalg.norm(normal_vector)
            
            angle_degrees = np.degrees(np.arccos(dot_product/(magnitude_horizontal*magnitude)))

            if angle_degrees > 85 or angle_degrees < -85:
                building_region = region_pcd.select_by_index(inliers)
                other_region = region_pcd.select_by_index(inliers, invert=True)
            else:
                other_region = region_pcd
                building_region = 0
                
            if building_region != 0: building_points.extend(building_region.points)
            other_points.extend(other_region.points)
    return building_points, other_points