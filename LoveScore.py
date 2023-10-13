
def Love(age, job, house,fang, car, auto,interests, location, visual_age, personality,beauty):
    # 年龄评分
    age=int(age)
    if age > 35:
        age_score = -5
    elif 18 <= age <= 26:
        age_score = 5
    else:
        age_score = 5 - (age - 25)
    # 工作评分
    job_scores = {"大金融或大厂": 10, "公务员": 8, "事业单位": 6, "国企单位": 4, "私企": 2,"灵活就业（读书ing）": 0}
    job_score = job_scores[job]
    # 住房评分
    house_scores = {"有房": 10, "没有": 0}
    house_score = house_scores.get(house,0)
    fang=int(fang)
    if house_score==0:
        fang_score=0
    else:
        if fang<15000:
            fang_score = 2
        elif fang>15000 and fang<20000:
            fang_score = 4
        elif fang > 20000 and fang < 25000:
            fang_score = 6
        elif fang > 25000 and fang < 30000:
            fang_score = 8
        elif fang > 30000 and fang < 35000:
            fang_score = 10
        elif fang > 35000 and fang < 50000:
            fang_score = 12
        else:
            fang_score=15
    auto_dict = {
        '其他': 2,
        '哪吒': 2,
        '比亚迪': 2,
        '大众': 3,
        '别克': 3,
        '雪佛兰': 3,
        '宝马3系': 4,
        '奥迪入门': 4,
        '奔驰入门': 4,
        '蔚小理': 5,
        '问界(遥遥领先)': 5,
        '特斯拉': 5,
        '宝马5系': 8,
        '奥迪A5': 8,
        '奔驰中级': 8,
        '宝马7系': 10,
        '奥迪A7': 10,
        '奔驰高级': 10,
        '保时捷': 10,
        '法拉利': 12,
        '兰博基尼': 15
    }
    # 车辆评分
    car_scores = {"有车": 10, "没有": 0}
    car_score = car_scores.get(car,0)
    if auto in auto_dict:
        auto_score = auto_dict[auto]
    else:
        # 处理或记录错误
        auto_score = 0
    # 兴趣评分  interests是一个列表  不同爱好的分数不一样
    interest_score=0
    正五分 = {"公益"}
    负五分={"蹦迪","喝酒","抽烟"}
    负二分={"瑜伽","棋牌","烘焙"}
    正二分={"公益","爬山（或骑车）","健身（或跑步）","美食烹饪","看书"}
    for interest in interests:
        if interest in 负二分:
            interest_score-=2
        if interest in 正二分:
            interest_score +=2
        if interest in 正五分:
            interest_score += 5
    if "旅游" in interests:
        if house_score==0 and job_score <4:
            interest_score-=2
    if interest_score>5:
        interest_score = 5
    if interest_score<-5:
        interest_score = -5
    if set(interests)& 负五分:
        interest_score =-5

        # 地区评分
    location_scores = {"北京市": 5, "上海市": 5, "浙江省": 3, "江苏省": 3, "广东省": 3}
    location_score = location_scores.get(location, 1)
    # 年龄差异评分
    visual_age=int(visual_age)
    age_diff = age - visual_age
    if age_diff > 5:
        age_diff = 5
    if  age_diff < -5:
        age_diff = -5
    if (visual_age>35 or age>35) and age_diff>0:
        age_diff=0
     # 性格评分
    personality_scores = {"活泼": 10,"真诚": 8,"内向": 5, "高冷": 2, "慢热": 0}
    personality_score = personality_scores.get(personality,0)
    # 颜值评分
    beauty_score = beauty * 0.4 if beauty >= 35 else 40 * 0.4
    # 总分
    total_score = beauty_score + age_score + job_score + fang_score + auto_score + interest_score + age_diff +personality_score+location_score
    total_score=round(total_score,3)
    return total_score

#######################################################################################################################################
#评价体系中，年龄5分  工作 10分   住房10分（15max）  汽车 10分   兴趣  10分   地区 5分   性格10分   颜值  40分



#######################################################################################################################################
# # Test example
# a=Love(34, "大金融或大厂", "有房", "有车", "娱乐类", "北京", 20, "慢热",68)
# print(round(a,2))
