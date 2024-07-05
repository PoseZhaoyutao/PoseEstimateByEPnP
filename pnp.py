# -*- coding: utf-8 -*-
# @Author  : Zhao Yutao
# @Time    : 2024/7/1 12:29
# @Function: 测试redis服务端发送图像
# @mails: zhaoyutao22@mails.ucas.ac.cn
import re
import cv2
import numpy as np
import cv2
import numpy as np

from scipy.spatial.transform import Rotation as R


def quaternion2euler(quaternion):
    r = R.from_quat(quaternion)
    euler = r.as_euler('xyz', degrees=True)
    return euler

#矩阵转四元数
def rot2quaternion(rot):
    r = R.from_matrix(rot)
    qua = r.as_quat()
    return qua
def rotvector2rot(rotvector):
    Rm = cv2.Rodrigues(rotvector)[0]
    return Rm
# print("真实R"+str([0.056550817 ,0.78191275 ,0.553326166, -0.281504193]))
# print("真实T"+str([-0.24170564, 0.218143689, 4.89465484 ]))
#相机内参
K = [[1744.92206139719, 0, 720.0], [0, 1746.58640701753, 540.0], [0, 0, 1]]
# img = cv2.imread(r"C:\Users\zhaoy\Desktop\AI4Space\stream-2-test\RT001\\img002_RT001.jpg")
# image_points_2D = np.array(
#     [
#         [640, 845], [469, 715], [1046, 560], [884, 391]
#     ],
#     dtype="double",
# )
# image_points_2D = np.array(
#     [[442,745],
#         [566,792],
#         [588,739],
#         [465,695]],
#     dtype="double",
# )
#帆板4角
figure_points_3D = np.array(
    [[-0.8005,-0.3024,-0.3933],
        [-0.8005,-0.3024,0.3975],
     [0.8044, -0.3024, -0.3933],
        [0.8044,-0.3024,0.3894]
    ]
)
# figure_points_3D = np.array(
#     [[0.2115,-0.2826,0.5405],
#         [-0.2014,-0.2826,0.5405],
#      [-0.1996, -0.2826, 0.3963],
#         [0.2154,-0.2826,0.3973]
#     ]
# )
point_list_file = open("fanban.txt","r")
point_list = []
for line in point_list_file.readlines():
    point_list.append(line.split("*"))
    print(point_list)
distortion_coeffs = np.zeros((4, 1))
matrix_camera = np.array(K)
RT_estimate = open(r"RT_estimate.txt","a")
for i in range(len(point_list)):
    image_name = point_list[i][0].split("/")[-1]
    # print(image_name)
    point = point_list[i][1].split("\n")[0]
    pattern = re.compile(r'\d+')
    nums = pattern.findall(point)
    # print(nums)
    image_points_2D = np.array(
        [[int(nums[0]),int(nums[1])],
            [int(nums[2]),int(nums[3])],
            [int(nums[4]),int(nums[5])],
            [int(nums[6]),int(nums[7])]],
        dtype="double",
    )
    success, vector_rotation, vector_translation = cv2.solvePnP(
        figure_points_3D, image_points_2D, matrix_camera, distortion_coeffs, flags=0
    )
    # 旋转矩阵到四元数
    r = R.from_matrix(rotvector2rot(vector_rotation))
    qua = r.as_quat()
    print("估计R"+str(qua))
    print("估计T"+str(vector_translation.T))
    RT_estimate.write(image_name+" "+str(vector_translation.T[0,0])+" "+str(vector_translation.T[0,1])+" "+str(vector_translation.T[0,2])+" "+
                    str(qua[0])+" "+str(qua[1])+" "+str(qua[2])+" "+str(qua[3])+"\n")

RT_estimate.close()
# nose_end_point2D, jacobian = cv2.projectPoints(
#     np.array([(0.0, 0.0, 1000.0)]),
#     vector_rotation,
#     vector_translation,
#     matrix_camera,
#     distortion_coeffs,
# )
# for p in image_points_2D:
    # cv2.circle(img, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)
# point1 = (int(image_points_2D[0][0]), int(image_points_2D[0][1]))
# point2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

# cv2.line(img, point1, point2, (255, 255, 255), 2)

# cv2.imshow("Final", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()