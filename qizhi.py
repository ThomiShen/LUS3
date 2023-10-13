import face_recognition
import os
current_path = os.path.dirname(os.path.abspath(__file__))
absolute_path = os.path.join(current_path, 'static')
# 存储前5张和后5张图片的face_encoding

face_images = [face_recognition.load_image_file(os.path.join(absolute_path,f"reference/气质{i}.jpg") )for i in range(1, 6)]
face_encodings = [face_recognition.face_encodings(img)[0] for img in face_images]

def get_most_similar_face(image_file):
    # 加载上传的图片
    up_image = face_recognition.load_image_file(image_file)
    up_encoding = face_recognition.face_encodings(up_image)[0]

    # 获取与上传图片的距离

    distances = face_recognition.face_distance(face_encodings, up_encoding)

    # 找到距离最小的图片索引
    index = distances.argmin()

    # 根据索引获取脸型和气质
    temperament = ["知性、优雅", "性感、活力", "高贵、淑女", "清纯、娇媚", "少女、甜美"][index]

    return  temperament
