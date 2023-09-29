import numpy as np
import open3d as o3d

def ransac(regions, row_number, threshold, iter_num):
    ground_points = []
    above_ground_points = []
    normal_vector_horizontal = np.array([0, 0, 1])
    for row in range(row_number):
        for col in range(row_number):
            region_points = np.asarray(regions[row][col])

            if len(region_points) >= 3:
                region_pcd = o3d.geometry.PointCloud()
                region_pcd.points = o3d.utility.Vector3dVector(region_points)

                plane_model, inliers = region_pcd.segment_plane(
                    distance_threshold=threshold, ransac_n=3, num_iterations=iter_num
                )
                normal_vector = np.array(plane_model[:-1])
                dot_product = np.dot(normal_vector_horizontal, normal_vector)
                magnitude_horizontal = np.linalg.norm(normal_vector_horizontal)
                magnitude = np.linalg.norm(normal_vector)
                
                angle_degrees = np.degrees(np.arccos(dot_product/(magnitude_horizontal*magnitude)))

                if angle_degrees > 20:
                    above_ground_region = region_pcd.select_by_index(inliers)
                    ground_region = region_pcd.select_by_index(inliers, invert=True)
                else:
                    ground_region = region_pcd.select_by_index(inliers)
                    above_ground_region = region_pcd.select_by_index(inliers, invert=True)
                
                ground_points.extend(ground_region.points)
                above_ground_points.extend(above_ground_region.points)
                
    return ground_points, above_ground_points