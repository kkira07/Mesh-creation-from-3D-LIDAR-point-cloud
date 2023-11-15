import numpy as np
import open3d as o3d

def cleaning(regions, row_number, z_max, z_min):
    outliers = []
    inliers = []
    for row in range(row_number):
        for col in range(row_number):
            z_max = 0
            z_min = 20
            region_points = np.asarray(regions[row][col])
            for point in region_points:
                if point[2] > z_max:
                    z_max = point[2]
                if point[2] < z_min:
                    z_min = point[2]
            for point in region_points:
                if z_max-z_min < 2.5 or point[2] - z_min < 0.2:
                    outliers.append(point)
                else:
                    inliers.append(point)

    pcd_in = o3d.geometry.PointCloud()
    pcd_in.points = o3d.utility.Vector3dVector(inliers)
    return pcd_in

            