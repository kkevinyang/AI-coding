from PIL import Image, ImageEnhance, ImageStat
import cv2
import numpy as np
import os

# Define the paths
input_folder = './pics'
output_folder = './pics_new'

# 定义目标亮度
target_brightness = 150
print(f"目标亮度: {target_brightness}")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def mod_brightness(image):
    # 转换为OpenCV格式
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 使用更简单的人脸检测方法
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 检测人脸
    faces = face_cascade.detectMultiScale(
        cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY),
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10)
    )

    if len(faces) > 0:
        # 获取所有人脸区域的边界
        x_min = min(face[0] for face in faces)
        y_min = min(face[1] for face in faces)
        x_max = max(face[0] + face[2] for face in faces)
        y_max = max(face[1] + face[3] for face in faces)
        
        # 扩大检测区域以包含更多主体部分
        height, width = opencv_image.shape[:2]
        x_min = max(0, x_min - 50)
        y_min = max(0, y_min - 100)  # 向上多扩展一些以包含上半身
        x_max = min(width, x_max + 50)
        y_max = min(height, y_max + 200)  # 向下多扩展一些以包含身体
        
        # 提取主体区域
        main_subject = opencv_image[y_min:y_max, x_min:x_max]
        
        # 计算主体区域的平均亮度
        main_subject_gray = cv2.cvtColor(main_subject, cv2.COLOR_BGR2GRAY)
        current_brightness = np.mean(main_subject_gray)
        print(f"主体区域当前平均亮度: {current_brightness:.2f}")
        
        # 计算需要的亮度调整系数
        if current_brightness < target_brightness:
            # 处理过暗的情况
            adjustment_factor = target_brightness / current_brightness
            # 限制调整系数在合理范围内
            adjustment_factor = min(1.5, max(1.0, adjustment_factor))
            print(f"图片偏暗，建议的亮度调整系数: {adjustment_factor:.2f}")
        elif current_brightness > target_brightness * 1.2:  # 允许20%的误差范围
            # 处理过亮的情况
            adjustment_factor = target_brightness / current_brightness
            # 限制调整系数在合理范围内
            adjustment_factor = max(0.6, min(1.0, adjustment_factor))
            print(f"图片偏亮，建议的亮度调整系数: {adjustment_factor:.2f}")
        else:
            # 亮度在目标范围内
            adjustment_factor = 1.0
            print("主体区域亮度适中，无需调整")
            
        # 调整整张图片的亮度
        enhancer = ImageEnhance.Brightness(image)
        adjusted_image = enhancer.enhance(adjustment_factor)
        
        # 检查调整后的亮度
        adjusted_opencv = cv2.cvtColor(np.array(adjusted_image), cv2.COLOR_RGB2BGR)
        adjusted_subject = adjusted_opencv[y_min:y_max, x_min:x_max]
        adjusted_brightness = np.mean(cv2.cvtColor(adjusted_subject, cv2.COLOR_BGR2GRAY))
        print(f"调整后主体区域的平均亮度: {adjusted_brightness:.2f}")
        
        # 保存调整后的图片
        adjusted_image.save(os.path.join(output_folder, filename))
    else:
        print("未检测到人脸，请检查图片")
    

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Open an image file
        print('---------------------------------------')
        print('开始处理图片:', filename)
        with Image.open(os.path.join(input_folder, filename)) as img:
            # Enhance the brightness
            mod_brightness(img)
            # enhancer = ImageEnhance.Brightness(img)
            # img_enhanced = enhancer.enhance(1.5)  # Adjust the factor as needed

            # # Save the enhanced image to the output folder
            # img_enhanced.save(os.path.join(output_folder, filename))
            