# PoseEstimateByEPnP
通过开发设计实现手动选择特征点，然后通过已知3D模型中的特征点进行匹配，最后利用EPnP求解相对位姿。
# PF_shoudong.py
类似Labelme一样设计，只不过很简单实现选点的工作，然后选择已挑选好的3D模型的特征角点保存至文件中
# pnp.py
选择好的特征角点提取出来与对应的3D模型的按照正确系来对应其三维空间下的位置，然后用EPnP问题求解相对位姿信息保存下来
# precision.py
评价位置与姿态误差，切记要保持格式正确，阅读一下代码！
