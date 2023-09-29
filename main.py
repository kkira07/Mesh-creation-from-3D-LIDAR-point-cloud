import numpy as np
import open3d as o3d
import pcd_division as pcddiv
import pcd_ransac as pcdran

pcd = o3d.io.read_point_cloud("output/campus_no_outliers.ply")
original_pcd = pcd

fine_tune_iter = 3 #try it again
iter_num = 1000
max_threshold = 0.5
min_threshold = 0.3
remaining_points = []
threshold = 10

for i in range(fine_tune_iter):
    row_number = (i*50)+100
    if i == fine_tune_iter-1: threshold = min_threshold
    else: threshold = max_threshold-(i*(max_threshold/fine_tune_iter))
    #if threshold > 0.7: threshold = max_threshold/row_number
    
    if i > 0 and i < fine_tune_iter*0.25: iter_num = 100
    elif i >= fine_tune_iter*0.25: iter_num = 20
    
    regions = pcddiv.pcd_division(pcd, row_number)
    ground_points, above_ground_points = pcdran.ransac(regions, row_number, threshold, iter_num)
    remaining_points.extend(above_ground_points)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(ground_points)
    print(f"Iteration {i+1} of {fine_tune_iter} is complete")
    print(f"Number of current regions: {row_number*row_number}, current iteration number: {iter_num}")

regions = pcddiv.pcd_division(pcd, 4)
ground_points, above_ground_points = pcdran.ransac(regions, 4, 1, 20)
remaining_points.extend(above_ground_points)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(ground_points)

above_ground_pcd = o3d.geometry.PointCloud()
above_ground_pcd.points = o3d.utility.Vector3dVector(remaining_points)

pcd.paint_uniform_color([0., 1., 0.])
above_ground_pcd.paint_uniform_color([1., 0., 0.])
o3d.visualization.draw_geometries([pcd, above_ground_pcd])
o3d.io.write_point_cloud("output/campus_ground_finetuned.ply", pcd)
o3d.io.write_point_cloud("output/campus_above_ground_finetuned.ply", above_ground_pcd)