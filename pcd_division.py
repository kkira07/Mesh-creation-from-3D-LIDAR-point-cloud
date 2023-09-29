import numpy as np
import open3d as o3d

def pcd_division(pcd, row_number):

    points = np.asarray(pcd.points)

    x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])

    x_step = (x_max - x_min) / row_number
    y_step = (y_max - y_min) / row_number

    regions = [[[] for _ in range(row_number)] for _ in range(row_number)]

    for point in points:
        x, y, _ = point
        row = int(-(x_min - x)/x_step)
        if row == row_number: row -= 1
        col = int(-(y_min - y)/y_step)
        if col == row_number: col -= 1
        
        regions[row][col].append(point)
                        
    return regions