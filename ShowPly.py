# -*- coding: utf-8 -*-
# @Author  : Zhao Yutao
# @Time    : 2024/7/1 12:29
# @Function: 测试redis服务端发送图像
# @mails: zhaoyutao22@mails.ucas.ac.cn
import open3d as o3d

pcd = o3d.io.read_point_cloud(r"C:\Users\zhaoy\Desktop\AI4Space\RT505_dense_gt.ply")

o3d.visualization.draw_geometries([pcd])