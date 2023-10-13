from flask import Flask, render_template, request,url_for,send_from_directory,jsonify,flash,redirect
import os
from face  import analyze_face
from qizhi import get_most_similar_face
from LoveSQL import LoveDatabase
from LoveScore import Love
from fang import  LianjiaScraper
from evaluation import  Evaluator

from auth import auth  # Import the auth blueprint
app = Flask(__name__)
app.register_blueprint(auth)    # Register the auth blueprint

app.secret_key = "123456"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        gender = request.form.get('gender')
        age = request.form.get('age')  # 获取滑块的值
        image_file = request.files.get('photo')
        fach = request.form.get('fach')  # 获取学历与专业的值
        job=request.form.get('job')
        personality = request.form.get('personality')
        house = request.form.get('house')
        car = request.form.get('car')
        interests=request.form.getlist('interests[]')    #兴趣爱好
        interest=' '.join(interests)
        location_codes = request.form.get('location').split('-')
        if len(location_codes) == 3:
            province_code, city_code, area_code = location_codes
        else:
            province_code = location_codes[0] if len(location_codes) > 0 else "浙江省"
            city_code = location_codes[1] if len(location_codes) > 1 else "杭州市"
            area_code = location_codes[2] if len(location_codes) > 2 else "西湖区"
        image_name_raw = image_file.filename
        image_name = image_name_raw.split('.')[0]
        # 保存图片到上传文件夹
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(filename)
        # 调用analyze_face函数分析人脸
        with open(filename, 'rb') as f:
            image_data = f.read()
        face_features = analyze_face(image_data)
        visual_age = face_features['age']
        beauty = face_features['beauty']
        #脸型英文转为中文！！！！！！！！！！！！
        face_shapes_dict = {
            "round": "圆脸型",
            "square": "方脸型",
            "oval": "椭圆脸型",
            "heart": "心形脸型",
            "long": "长脸型",
            "diamond": "钻石脸型"
        }
        face_shape = face_features['face_shape']['type']
        face_shape=face_shapes_dict[face_shape]
        # glasses = face_features['glasses']['type']
        # 气质调用分析
        temperament=get_most_similar_face(image_file)
        #居住地址
        home=request.form.get('home')
        #居住价格
        f=LianjiaScraper()
        fang=f.fetch_prices(province_code, city_code,home)
        # User的汽车类型
        auto=request.form.get("auto")
        #OPENAI大模型
        api_key = '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'
        # 读取你的提示prompt
        address=f'/Users/thomi/Desktop/1.txt'
        with open(address, "r") as f:
            prompt = f.read()
        personal_information="|".join([image_name,gender,str(age),job, house,str(fang), car, auto,personality,interest, province_code, str(visual_age),str(beauty)])
        prompt=prompt+personal_information
        eva=Evaluator(api_key)
        evaluation=eva.get_evaluation(prompt)
        if fang is not None:
            Fang = int(fang)
        else:
            Fang = 0  # 或者您可以为它分配其他默认值或采取其他适当的操作
        scores=Love(age,job,house,10000,car,auto,interests,province_code,visual_age,personality,beauty)
        db=LoveDatabase(host='localhost', port=3306, user='root', password='12345678', database='test')
        db.insert_data(image_name,gender,age,fach,job, house, car, interest, province_code, visual_age, beauty,image_data,home,fang,evaluation)
        db.close()
        if gender and filename and age and house and car and interest:
            gender = f"{'男' if gender == 'male' else '女'}"
            age=f"{age}"
            return render_template('result.html', selected_gender=gender,selected_age=age,selected_name=image_name,selected_image=filename,selected_job=job,
             selected_personality=personality,selected_house=house,selected_car=car,selected_interest=interest,
                                    selected_province=province_code,selected_city=city_code,selected_area=area_code,
                                   selected_visual_age=visual_age ,selected_beauty=beauty,
                                   selected_face_shape=face_shape,selected_temperament=temperament,
                                   selected_score=scores,selected_home=home,selected_fang=fang,
                                   selected_auto=auto,selected_evaluation=evaluation,selected_fach=fach)
        else:
            flash('请选择性别!')
            return redirect(url_for('index'))

    return render_template('result.html', selected_name=None,selected_gender=None,selected_age=None,
                           selected_job=None,selected_personality=None,selected_house=None,
                           selected_car=None,selected_interest=None,
                           selected_province=None,selected_city=None,selected_area=None,
                           selected_visual_age=None, selected_beauty=None, selected_face_shape=None,selected_temperament=None,
                           selected_score=None,selected_home=None,selected_fang=None,selected_auto=None,
                           selected_evalution=None,selected_fach=None
                           )
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
