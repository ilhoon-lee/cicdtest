from flask import Flask, render_template, request, redirect, flash, url_for, make_response, session #render_template으로 html파일 렌더링
import mysql.connector
import boto3
import datetime
import random
import inspect
import os
import string
import random
import time
import json
import base64
import requests
from PIL import Image

# 일훈 __PATH__ = 'C:/Users/user/Desktop/test/'
# 진철 __PATH__ = '/usr/src/flask_app/user-upload'
# 광현 __PATH__ = 'D:/프로젝트/6_최종/version/test/test_v7_4'
__PATH__ = 'D:/프로젝트/6_최종/version/test/test_v7_4'
os.chdir(__PATH__)
os.getcwd()
import Kkanocr
import Recom1
import Mypage
#import text_filter

server = Flask(__name__)
server.config["SECRET_KEY"] = "ABCD"
server.secret_key = "kkanbu"


def mysql_connetion():
    try:
        mydb = mysql.connector.connect(
            host="mysql.cbtzgcvtawc2.ap-northeast-2.rds.amazonaws.com",
            user="root",
            passwd="pass123#",
            database="recipe"
        )
    except Exception as e:
        print(e)
    else:
        return mydb


AWS_ACCESS_KEY = 'AKIATW6JX2WRN63ZNUXR'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_BUCKET_REGION = "ap-northeast-2"
AWS_S3_BUCKET_NAME = "user-test3467"

def s3_connection():
    '''
    s3 bucket에 연결
    :return: 연결된 s3 객체
    '''
    try:
        s3 = boto3.client(
            service_name='s3',
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    except Exception as e:
        print(e)
        exit(ERROR_S3_CONNECTION_FAILED)
    else:
        print("s3 bucket connected!")
        return s3

def s3_put_object(s3, bucket, filepath, access_key):
    '''
    s3 bucket에 지정 파일 업로드
    :param s3: 연결된 s3 객체(boto3 client)
    :param bucket: 버킷명
    :param filepath: 파일 위치
    :param access_key: 저장 파일명
    :return: 성공 시 True, 실패 시 False 반환
    '''
    try:
        s3.upload_file(filepath, bucket, access_key)
    except Exception as e:
        print(e)
        return False
    return True

s3 = s3_connection()


def Expiration_Date(ingr):
    #ingr='캔참치'
    mydb=mysql_connetion()
    cur = mydb.cursor()
    try:
        cur.execute(f"SELECT * FROM ingredients WHERE name='{ingr}'")
        temp = cur.fetchall()
        
        ingr_num = temp[0][0]
        ingr_score = temp[0][2]
        exp_date = temp[0][3]
        
    except:
        ingr_num = 0
        ingr_score = 9
        exp_date = 14
    cur.close()
    return ingr_num, ingr_score, exp_date;


def random_code():
    string_pool = string.ascii_letters + string.digits
    r_code = ''
    for i in range(20):
        r_code += random.choice(string_pool)
    return r_code


def text_reconize(img):
    URL = "https://up8wh3ooec.apigw.ntruss.com/custom/v1/13236/52b0ee39e1a14ae9e57428f32e0a1d6cc2c15b6d81c060cb7b20a1b8ee67b9bc/general"
    KEY = "d1FYa0dldWV0VlpvRVV2clZ0bUhubUFSVFltem16em8="
    headers = {
        "Content-Type": "application/json",
        "X-OCR-SECRET": KEY
    }    
    data = {
        "version": "V1",
        "requestId": "sample_id", 
        "timestamp": 0, 
        "images": [
            {
                "name": "sample_image",
                "format": "png",
                "data": img.decode('utf-8')
            }]}
    
    data = json.dumps(data)
    response = requests.post(URL, data=data, headers=headers)
    res = json.loads(response.text)
    fields=res['images'][0]['fields']

    name=[]           
    for i in range(len(fields)):
        name.append(fields[i]['inferText'])
    text = []
    for i in range(len(name)):
        if tf.text_filter(name[i]) is not None:
            text.append(tf.text_filter(name[i]))
        textkind=list(set(text))
    return textkind


def unknown_user_create():
    now=datetime.datetime.now()
    nowDatetime = now.strftime('%y/%m/%d-%H:%M:%S')
    random.randrange(0,1000000)
    return (str(nowDatetime)+'-'+str(random.randrange(0,1000000)))


# def Matching_Score(user,friend_id):
#     mydb=mysql_connetion()
#     cur = mydb.cursor()
    
#     # user의 재료 검색
#     cur.execute("SELECT ingredients FROM user_ingredients where id like '"+user+"';") #음식 재료 DB에서 출력
#     ingr_temp = cur.fetchall()
#     #######
#     user_ingr = list(map(lambda x: ingr_temp[x][0],range(len(ingr_temp)))) # 음식재료 리스트로 변환
    
    
#     cur.execute("SELECT * FROM ingredients ")
#     food_ingredients_temp = cur.fetchall()
#     print(len(food_ingredients_temp))
    
    
#     x = pd.DataFrame(food_ingredients_temp)                 
    
#     xx = x[ x[0] ==1 ] # 주재료1 소고기 돼지고기 닭고기
#     xx2 = x[x[0]==2 ] # 주재료2 해산물
#     lisx1 = list(xx[1]) + list(xx2[1])
#     xx3 = x[x[0]==8] #향신료 8
#     xx4 = x[x[0]==9] #소스 9
#     lisx2 = list(xx3[1]) + list(xx4[1])
    
    
#     #####################################기본  matching_score######################
#     My_matching_score=0  # 나의 매칭 스코어
#     for i in range(len(user_ingr)):
#         if user_ingr[i] in lisx1:
#             print("자신의 메인재료 +10점 ",user_ingr[i])
#             My_matching_score+=10
#             print(My_matching_score)
#         elif user_ingr[i] in lisx2:
#             print("자신의 조미료 +0점", user_ingr[i])
#             print(My_matching_score)
#         else:
#             print("자신의 부재료 +1", user_ingr[i])
#             My_matching_score+=1
#             print(My_matching_score)
#     My_matching_score
#      ##################################상대적 matching_score######################
#     #friend_id= "kmr_friend" #친구 id
#     cur.execute("SELECT * FROM user_ingredients where id like '"+friend_id+"';") # 친구 음식 재료 DB에서 출력
#     friend_ingr_temp = cur.fetchall() #친구 list DB에서 출력
#     cur.close()
#     type(friend_ingr_temp)
#     #######
#     Friend_matching_score=0  # 친구 매칭 스코어
#     friend_ingr= list(map(lambda x : friend_ingr_temp[x][2], range(len(friend_ingr_temp)))) 
#     # 음식재료 1차원 리스트로 변환 
#     for i in range(len(friend_ingr)):
#         if user_ingr[i] not in lisx1 and friend_ingr[i] in lisx1:
#                 print("자신은 주재료가 없고 상대방은 주재료가 있을 경우 +10점",friend_ingr[i])
#                 Friend_matching_score+=10
#                 print(Friend_matching_score)
#         if friend_ingr[i] in lisx1:
#             print("친구 메인재료 +10점 ",friend_ingr[i])
#             Friend_matching_score+=10
#             print(Friend_matching_score)
            
#         elif user_ingr[i] in lisx2:
#             print("친구 조미료 +0점", friend_ingr[i])
#             print(Friend_matching_score)
#         else:
#             print("친구 부재료 +1점", friend_ingr[i])
#             Friend_matching_score+=1
#             print(Friend_matching_score)
#     Friend_matching_score
#     return Friend_matching_score


def make_query(find_value,table,where_list="",where_value="",order="",limit = ""):
    que1 = "SELECT " + find_value + " FROM " + table 

    if where_list != "":
        que1 = que1 + " WHERE"
        for i in range(len(where_list)):
            if i == 0:
                que1 = que1 + " " + where_list[i] + " = " + where_value[i] 
            else:
                que1 = que1 + " AND " + where_list[i] + " = " +  where_value[i]
        

    if order != "" and str(limit) != "":
        que1 = que1 + " ORDER BY " + order + " LIMIT " +str(limit)
    elif order != "" and str(limit) == "":
        que1 = que1 + " ORDER BY " + order    
        
        
    que1 = que1 + ";"        
    return(que1)

def get_count(my_list):
    new_list = {}
    for i in my_list:
        try: new_list[i] += 1
        except: new_list[i] = 1

    return(new_list)

def randomrec():  
    import random
    per = [4, 1.8742, 4, 4, 2.25004, 3.70396, 0.6566, 5, 3.9754, 5, 5, 4, 5, 4, 4, 4, 3.90232, 4, 4, 4, 0.8654, 0.90716, 0.12088, 0.12088, 0.75056, 3.80836, 0.11044,2.430279,0.19396, 0.74012, 0.698359, 0.68792, 0.12088, 0.13132, 2.31268, 2.11432, 5, 3.871, 1.98904, 1.90552, 0.18352, 2.25, 0.12088, 2.07256, 3.46384, 1.85332, 0.71924, 0.12088]
    code = ['101', '102', '103', '104', '105', '106', '107', '201', '202', '203', '204', '205', '206', '207', '301', '302', '303', '304', '305', '306', '307', '411', '412', '413', '414', '415', '416', '421', '422', '423', '424', '425', '426', '427', '431', '432', '433', '434', '435', '436', '437', '441', '442', '443', '444', '445', '446', '447']
    
    ##골고루 28개 뿌리는거
    list1 = [] 
    for i in range(1,5):
        for j in range(1,8):
            if i == 4 and j == 7:
                list1.append(str(i) + str(random.randint(2,4)) + str(j))
            elif i ==4 and j != 7:
                list1.append(str(i) + str(random.randint(1,4)) + str(j))
            else:
                list1.append(str(i) + str(0) + str(j))
                
    list2= random.choices(code,weights=per,k=72)
    k = list1+list2
    querylist = get_count(k)
    where_list = ["code_main","code_sub","code_cook"]
    
    ranrec = []
    
    for key, value in querylist.items():
        
        if value >=1:
            where_value = []
            #print(key, value, end = " /")          #num = num+value
            #print(key[0],key[1],key[2],value)
            where_value.append(key[0])
            where_value.append(key[1])
            where_value.append(key[2])
            #print( make_query("*","recipe",where_list,where_value,order="rand()",limit=value) )
            mydb = mysql_connetion()
            cur = mydb.cursor()
            cur.execute( make_query("*","recipe",where_list,where_value,order="rand()",limit=value) )
            xxx = cur.fetchall()
            cur.close()
            for i in range(value):
                ranrec.append([ xxx[i][0],xxx[i][2],xxx[i][3],xxx[i][4],xxx[i][1] ])
             
    random.shuffle(ranrec)
    
    return ranrec

def rec70():
    T = True
    while T:
        try:
            rec70 = randomrec()
            print("ok")
            T = False
        except:
            print("error")
            pass
    
    return rec70

def user_select(userid,rec2,choice):
    mydb = mysql_connetion()
    cur = mydb.cursor()
    now=datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    recipenum = int(choice[-1])
    rec2[ rec2.index(choice) +1 ]
    rec2[ rec2.index(choice) +2 ]
    rec2[ rec2.index(choice) +3 ]
    code_main = rec2[ rec2.index(choice) +1 ]
    code_sub = rec2[ rec2.index(choice) +2 ]
    code_cook = rec2[ rec2.index(choice) +3 ]
    sql = 'INSERT INTO user_select(id,number,code_main,code_sub,code_cook) VALUES(%s, %s, %s, %s, %s, %s)'
    val = (userid,recipenum,code_main,code_sub,code_cook, nowDatetime)
    cur.execute(sql, val)
    mydb.commit()
    cur.fetchall()  
    cur.execute("SELECT * FROM user_select where id like '"+userid+"' order by id desc limit 1;")
    lastadd = cur.fetchall()  
    cur.close()
    print(lastadd)


@server.route('/')
def start():
    session['user_id'] = "unknown_user"
    session['login_flag'] = False
    session['ingredient'] = []
    session['find_r'] = False # 기본 추천 레시피flag
    session['fri_propose'] = False
    session['mypage_message'] = False
    return render_template("start.html")

@server.route('/index', methods=['GET', 'POST'])
def index():
    login_flag = session['login_flag']
    user_id = session['user_id']
    ingredient = session['ingredient']
    
    mydb = mysql_connetion()
    cur = mydb.cursor()
    
    path = 'https://recipe-thumbnail.s3.ap-northeast-2.amazonaws.com/image/'
    
    if login_flag == True:
        try:
            ing_list=''
            cur.execute(f"select ingredients from user_ingredients where id ='{user_id}';")
            ing_list = cur.fetchall()
            
            ing_str = ', '.join(list(map(lambda x: ing_list[x][0], range(len(ing_list)))))
            print("내 재료 조회 성공")
        except:
            ing_str = ''
            print("내 재료 조회 실패")
        
        #####나혼자하는거
        try:
            loginuser_rec = Recom1.user_info(f'{user_id}')
            img_list1 = list(map(lambda x : path+str(loginuser_rec[x][0])+'.jpg', range(0, 10)))
            img_values1 = list(map(lambda x : str(loginuser_rec[x][0]), range(0, 10)))
            img_titles1 = list(map(lambda x : str(loginuser_rec[x][1])[:8]+'...', range(0, 10)))
        except:
            img_list1 = []
            img_values1 = []
            img_titles1 = []
        
        # 친구리스트, 친구들의 재료, 친구의 매칭점수, 추천유저, 추천유저 재료, 추천유저 매칭점수
        friend_list, friends_str_list, friend_score, top5id, top5user_str_list, top5score = Recom1.friend_rank5user(user_id)
        
        
        #### 깐부들 or 추천유저들과 레시피 보기 클릭시
        if request.method == 'POST':
            # 깐부들과 추천 레시피 보기를 클릭했을 경우
            try:
                users = request.form.getlist("friends")
                if users:
                    print(f'체크된 친구목록: {users}')
                    usermatch_rec = Recom1.user_match(users)
                    img_list2 = list(map(lambda x : path+str(usermatch_rec[x][0])+'.jpg', range(0, 10)))
                    img_values2 = list(map(lambda x : str(usermatch_rec[x][0]), range(0, 10)))
                    img_titles2 = list(map(lambda x : str(usermatch_rec[x][1])[:8]+'...', range(0, 10)))
                else: 
                    img_list2 = []
                    img_values2 = []
                    img_titles2 = []
                    users = []
            except:
                img_list2 = []
                img_values2 = []
                img_titles2 = []
                users = []
            # 추천유저와 추천 레시피 보기를 클릭했을 경우
            try:
                top_user = request.form.get("top_user")
                if top_user:
                    top_user = [top_user]
                    print(f'추천된 유저목록: {top_user}')
                    topmatch_rec = Recom1.user_match(top_user)
                    img_list6 = list(map(lambda x : path+str(topmatch_rec[x][0])+'.jpg', range(0, 10)))
                    img_values6 = list(map(lambda x : str(topmatch_rec[x][0]), range(0, 10)))
                    img_titles6 = list(map(lambda x : str(topmatch_rec[x][1])[:8]+'...', range(0, 10)))
                else:
                    img_list6 = []
                    img_values6 = []
                    img_titles6 = []
                    top_user = []
            except:
                img_list6 = []
                img_values6 = []
                img_titles6 = []
                top_user = []
                
        # 깐부들 or 추천유저들과 레시피 보기를 클릭 안했을 경우
        else:
            img_list2 = []
            img_values2 = []
            img_titles2 = []
            users = []
            img_list6 = []
            img_values6 = []
            img_titles6 = []
            top_user = []
    # 비로그인 사용자
    else: 
        if ingredient:    # 재료 있으면
            unknown = Recom1.unknown_info(ingredient)
            img_list1 = list(map(lambda x : path+str(unknown[x][0])+'.jpg', range(0, 10)))
            img_values1 = list(map(lambda x : str(unknown[x][0]), range(0, 10)))
            img_titles1 = list(map(lambda x : str(unknown[x][1])[:8]+'...', range(0, 10))) 
        else:
            img_list1 = []
            img_values1 = []
            img_titles1 = []
        
        # 비로그인 사용자가 사용하지 않는 변수들
        friend_list=[]
        friends_ing_list=[[]]
        friends_str_list=['']
        friend_score=[]
        top5id=[]
        top5user_str_list=['']
        top5score=[]
        ing_str =''
        ing_str = ', '.join(ingredient)
        img_list2 = []
        img_titles2 = []
        img_values2 = []
        img_list3 = []
        img_titles3 = []
        img_values3 = []
        img_list4 = []
        img_titles4 = []
        img_values4 = []
        img_list5 = []
        img_titles5 = []
        img_values5 = []
        img_list6 = []
        img_values6 = []
        img_titles6 = []
        users = []
        top_user = []
    
    if session['find_r'] is False:
        #### 우리 서비스에추서 추천 
        cur.execute('select * from recipe order by rand() limit 10;')
        rand_list3 = cur.fetchall()
        img_list3 = list(map(lambda x : path+str(rand_list3[x][0])+'.jpg', range(0, 10)))
        img_values3 = list(map(lambda x : str(rand_list3[x][0]), range(0, 10)))
        img_titles3 = list(map(lambda x : str(rand_list3[x][1])[:8]+'...', range(0, 10)))
        session['find_r3'] = [img_list3, img_values3, img_titles3]
        ####
        cur.execute('select * from recipe order by rand() limit 10;')
        rand_list4 = cur.fetchall()
        img_list4 = list(map(lambda x : path+str(rand_list4[x][0])+'.jpg', range(0, 10)))
        img_values4 = list(map(lambda x : str(rand_list4[x][0]), range(0, 10)))
        img_titles4 = list(map(lambda x : str(rand_list4[x][1])[:8]+'...', range(0, 10)))
        session['find_r4'] = [img_list4, img_values4, img_titles4]
        ####
        cur.execute('select * from recipe order by rand() limit 10;')
        rand_list5 = cur.fetchall()
        img_list5 = list(map(lambda x : path+str(rand_list5[x][0])+'.jpg', range(0, 10)))
        img_values5 = list(map(lambda x : str(rand_list5[x][0]), range(0, 10)))
        img_titles5 = list(map(lambda x : str(rand_list5[x][1])[:8]+'...', range(0, 10)))
        session['find_r5'] = [img_list5, img_values5, img_titles5]
        
        session['find_r'] = True
    else:
        img_list3 = session['find_r3'][0]
        img_values3 = session['find_r3'][1]
        img_titles3 = session['find_r3'][2]
        img_list4 = session['find_r4'][0]
        img_values4 = session['find_r4'][1]
        img_titles4 = session['find_r4'][2]
        img_list5 = session['find_r5'][0]
        img_values5 = session['find_r5'][1]
        img_titles5 = session['find_r5'][2]
        
    if session['fri_propose']:
        flash(session['fri_propose'])
        session['fri_propose'] = False
        
    cur.close()
    return render_template("index.html", login_flag=login_flag, user=user_id, ingredient=ing_str, img_list1=img_list1, img_values1=img_values1, img_titles1=img_titles1, img_list2=img_list2, img_values2=img_values2, img_titles2=img_titles2, img_list3=img_list3, img_values3=img_values3, img_titles3=img_titles3, img_list4=img_list4, img_values4=img_values4, img_titles4=img_titles4, img_list5=img_list5, img_values5=img_values5, img_titles5=img_titles5, img_list6=img_list6, img_values6=img_values6, img_titles6=img_titles6, friend_list=friend_list, friends_str_list=friends_str_list, friend_score=friend_score, users=users, top5id=top5id, top5user_str_list=top5user_str_list, top5score=top5score, top_user=top_user)

@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mydb = mysql_connetion()
        cur = mydb.cursor()
        
        userid = request.form.get("id")
        userpw = request.form.get("pw")
        
        # 아이디 확인
        cur.execute('select id from user_info;')
        ids = cur.fetchall()
        id_list = list(map(lambda x : ids[x][0], range(len(ids))))
            
        if userid not in id_list:
            flash("아이디를 확인해주세요")
            print('아이디 틀림')
            userid=''
            cur.close()
            return render_template("login.html")
        
        # 비밀번호 확인
        cur.execute(f"select password from user_info where id='{userid}';")
        pw = cur.fetchall()
        if userpw != pw[0][0]:
            flash("비밀번호를 확인해주세요")
            print('비밀번호 틀림')
            userpw=''
            cur.close()
            return render_template("login.html")
        
        
        session['user_id'] = userid
        session['login_flag'] = True # 로그인
        session['ingredient'] = False 
        print('로그인됨')
        cur.close()
        return redirect("/index")
    else:
        return render_template("login.html")
    
@server.route('/logout')
def logout():
    session['login_flag'] = False
    session['user_id'] = "unknown_user"
    session['ingredient'] = []
    return redirect('/index')

@server.route('/join', methods=['GET', 'POST'])
def join():
    today = datetime.datetime.today()
    today = today.strftime('%Y-%m-%d')
    if request.method == 'POST':
        userid = request.form.get('userid') 
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        username = request.form.get('username')
        address = request.form.get('address')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')     
        id_flag = request.form.get('id_flag') 
        nick_flag = request.form.get('nick_flag')
        id_temp = request.form.get('id_temp') 
        nick_temp = request.form.get('nick_temp')
        
        
        if id_temp != userid:
            id_flag = 'False'
            id_temp = userid
        else:
            id_temp = userid
            
        if nick_temp != nickname:
            nick_flag = 'False'
            nick_temp = nickname
        else:
            nick_temp = nickname
            
        mydb = mysql_connetion()
        cur = mydb.cursor()
        if id_flag == 'False':
            cur.execute('select id from user_info;')
            ids = cur.fetchall()
            id_list = []
            for i in ids:
                id_list.append(i[0])
                
            if userid in id_list:
                flash("아이디가 중복입니다.")
                print('아이디 중복')
                userid=''
                cur.close()
                return render_template("join.html", id_flag=id_flag, id_temp=id_temp, nick_flag=nick_flag, nick_temp=nick_temp, userid=userid, nickname=nickname, username=username, address=address, birthday=birthday, gender=gender, phone_number=phone_number, email=email)
            else:
                id_flag='True'
        else:
            pass
            
        if nick_flag == 'False':
            cur.execute('select nickname from user_info;')
            nicks = cur.fetchall()
            nick_list = []
            for n in nicks:
                nick_list.append(n[0])
                
            if nickname in nick_list:
                flash("닉네임 중복입니다.")
                print('닉네임 중복')
                nickname=''
                cur.close()
                return render_template("join.html", id_flag=id_flag, id_temp=id_temp, nick_flag=nick_flag, nick_temp=nick_temp, userid=userid, nickname=nickname, username=username, address=address, birthday=birthday, gender=gender, phone_number=phone_number, email=email)
            else:
                nick_flag='True'
        else:
            pass
        
        if gender == "선택":
            flash("성별을 선택해주세요.")
            print("성별 미선택")
            cur.close()
            return render_template("join.html", id_flag=id_flag, id_temp=id_temp, nick_flag=nick_flag, nick_temp=nick_temp, userid=userid, nickname=nickname, username=username, address=address, birthday=birthday, phone_number=phone_number, email=email)
        
        try:
            cur.execute(f"INSERT INTO user_info(id, password, nickname, name, address, date_of_birth, sex, phone_number, email) VALUES ('{userid}', '{password}', '{nickname}', '{username}', '{address}', '{birthday}', '{gender}', '{phone_number}', '{email}');")
            mydb.commit()
            print('회원정보 업로드')
        except:
            print("회원정보 업로드 실패")
        
        session['new_user'] = userid
        session['choice'] = []
        cur.close()
        return redirect('/select')
    else:
        userid=''
        password=''
        nickname=''
        username=''
        address=''
        birthday=''
        gender=''
        phone_number=''
        email=''
        id_flag = 'False'
        id_temp = ''
        nick_flag = 'False'
        nick_temp = ''
        return render_template("join.html", id_flag=id_flag, id_temp=id_temp, nick_flag=nick_flag, nick_temp=nick_temp, userid=userid, password=password, nickname=nickname, username=username, address=address, birthday=birthday, phone_number=phone_number, email=email, today=today)
    

@server.route('/select', methods=['GET', 'POST'])
def select():
    userid = session['new_user']
    choice = session['choice']
    #userid = 'irt'
    #choice =[]
    global rec2
    global rec100

    mydb = mysql_connetion()
    cur = mydb.cursor()
    
    cur.execute('SELECT * FROM recipe ORDER BY RAND() LIMIT 10;')
    img = cur.fetchall()
    path = 'https://recipe-thumbnail.s3.ap-northeast-2.amazonaws.com/image/'
    
    img_list = []
    img_values = []
    
    if request.method=='POST':
        choice.append( request.form.get('choice') )
        session['choice'] = choice
        #choice.append( '6946885' )
        print(choice)
        ##
        recipenum = int(choice[-1])
        code_main = rec2[ rec2.index(recipenum) +1 ]
        code_sub = rec2[ rec2.index(recipenum) +2 ]
        code_cook = rec2[ rec2.index(recipenum) +3 ]
        sql = 'INSERT INTO user_select(id,number,code_main,code_sub,code_cook) VALUES(%s, %s, %s, %s, %s)'
        val = (userid,recipenum,code_main,code_sub,code_cook)
        cur.execute(sql, val)
        mydb.commit()
        ###
        if len( choice ) == 10:
            session['choice'] = []
            rec100 = []
            img_list = []
            img_values = []
            session['user_id'] = session['new_user']
            session['new_user'] = False
            session['login_flag'] = True
            cur.close()
            return redirect('/index')
        else:
            ##choice가 선택한 레시피 번호

            img_list = list(map(lambda x : path+str(rec100[x][0])+'.jpg', range(len(choice)*10 , len(choice)*10+10)))
            img_values = list(map(lambda x : str(rec100[x][0]), range(len(choice)*10 , len(choice)*10+10)))
            img_titles = list(map(lambda x : str(rec100[x][4])[:10]+'...', range(len(choice)*10 , len(choice)*10+10)))             
            
            #user_select(userid,rec2,choice)
            ##진철이한테 줘야되는게 유저이름,클릭시간, 레시피번호,코드1, 2, 3 
            cur.close()
            return render_template("select.html", choice=len(choice), img_list=img_list, img_values=img_values, img_titles=img_titles)
        
    else:
        rec100 = rec70()
        rec2 = sum(rec100,[])
        img_list = list(map(lambda x : path+str(rec100[x][0])+'.jpg', range(len(choice)*10 , len(choice)*10+10)))
        img_values = list(map(lambda x : str(rec100[x][0]), range(len(choice)*10 , len(choice)*10+10)))
        img_titles = list(map(lambda x : str(rec100[x][4])[:10]+'...', range(len(choice)*10 , len(choice)*10+10)))
        cur.close()
        return render_template("select.html", choice=len(choice), img_list=img_list, img_values=img_values, img_titles=img_titles)


@server.route('/upload')
def upload():
    user = session['user_id']
    login_flag = session['login_flag']
    return render_template("upload.html", login_flag=login_flag, user=user)


@server.route('/input', methods=['GET', 'POST'])
def input_ing():
    import datetime
    user = session['user_id']
    
    if request.method=='POST':
        user_id = session['user_id']
        
        ##유저가 재료사진을 업로드할 때 : 시간값 저장 

        ####test 위한 경로
        #os.getcwd()
        #os.chdir('C:/Users/user/Desktop/test/test_v7_3')
        
        ###우리 EC2 저장경로 진철 수정해야함
        ##container_path = 'ECs 컨테이너에서 저장경로'
        now=datetime.datetime.now()
        nowDatetime = now.strftime('%Y%m%d%H%M%S')         
        
        container_path = __PATH__ + '/'
        
        #user_id = "leeilhoon123"
        aws_save_name=(user_id+'_'+nowDatetime+'.jpg')
        
        local_save_name = container_path + aws_save_name
        
        f = request.files['file']
 
        f.save(local_save_name)
        
        f = Image.open( local_save_name )
        #ff = f.resize((int(f.size[0]*0.9),int(f.size[1]*0.9)))
        while True:
            if (f.size[0] * f.size[1]) > 409600:
                v = 0.9
                if (f.size[0] * f.size[1]) > 1690000:
                    v = 0.5
                    if (f.size[0] * f.size[1]) > 2138400:
                        v = 0.4
                        #if (f.size[0] * f.size[1]) > 12192768:
                f = f.resize((int(f.size[0]*v),int(f.size[1]*v)))
                print(f'resizing size: {f.size[0]}, {f.size[1]}')
            else:
                print('image 저장')
                break

        ret = s3_put_object(s3, AWS_S3_BUCKET_NAME, local_save_name, 'tempimage/'+aws_save_name)
        
        if ret :
            print("tempimage 저장 성공")
            ret=''
        else:
            print("tempimage 저장 실패")
        
            
        ## S3에 유저아이디-시간.jpg 로저장
        ret = s3_put_object(s3, AWS_S3_BUCKET_NAME, local_save_name, 'testimage/'+aws_save_name)
        if ret :
            print("testimage 저장 성공")
            ret=''
        else:
            print("testimage 저장 실패")
            
            
            
        # if Recom1.yoloresult(aws_save_name, container_path ) == None:
        #     yoloresult = None
        # else:
        #     result_ingr, result_ingrnum = Recom1.yoloresult(aws_save_name, container_path )
        #     yoloresult = result_ingr           
        
        result_ingr,result_ingrnum= Recom1.yoloresult(aws_save_name, container_path )
        
        
        ### 값을 받아 YOLO알고리즘 동작해야함. 
        ##### OCR 들어가야 될 부분 #####
        with open(local_save_name, "rb") as f:
            testimg = base64.b64encode(f.read())  
        ocrresult = Kkanocr.text_reconize(testimg)
        
        ## yolo 추가해야됨  
        # 값을 받아 YOLO알고리즘 동작해야함. 
        
        ##개수표시
        #yoloresult = list(map(lambda x : str(result_ingr[x])+ " "+str(result_ingrnum[x])+"개",range(len(result_ingr))))
        yoloresult = result_ingr
        
        ##최종 도출되는 것
        values =[]
        if ocrresult == None and yoloresult == None:
            values =[]# YOLO 알고리즘에 의해 판별된 식재료가 리스트형식으로 받아짐
        elif ocrresult == None and yoloresult != None:
            values =   yoloresult# YOLO 알고리즘에 의해 판별된 식재료가 리스트형식으로 받아짐
        elif ocrresult != None and yoloresult == None:
            values = ocrresult# YOLO 알고리즘에 의해 판별된 식재료가 리스트형식으로 받아짐
        else:
            values =  ocrresult + yoloresult
             
        values = list(set(values))

        os.remove(local_save_name)
    else:
        values=[]
    return render_template("input.html", values=values)




@server.route('/ing_save', methods=['POST'])
def ing_save():
    if request.method=='POST':
        login_flag = session['login_flag']
        user_id = session['user_id']
        
        mydb = mysql_connetion()
        cur = mydb.cursor()
        # 기존 데이터는 삭제
        if login_flag == True:
            try:
                cur.execute(f"delete from user_ingredients where id = '{user_id}';")
                mydb.commit()
                print("기존 재료들 삭제")
            except:
                print("기존 재료들 삭제 실패")
        else:
            session['ingredient'] = []
            
            
        # 새로운 데이터 삽입
        ing = request.form.getlist('ingredient')
        ing = list(filter(None, ing))
        if login_flag == True:
            for i in ing:
                try:
                    ingr_num, ingr_score, exp_date = Expiration_Date(i)
                    timeinput = datetime.datetime.now()
                    ex = datetime.datetime.now()+datetime.timedelta(exp_date)
                    exday= datetime.datetime.strftime(ex.replace(microsecond=0), '%Y-%m-%d %H:%M:%S')
                    cur.execute(f"INSERT INTO user_ingredients(id, ingredients,update_date, expiration_date, ingr_num,ingr_score) VALUES('{user_id}', '{i}', '{timeinput}','{exday}', '{ingr_num}' ,'{ingr_score}');")
                    mydb.commit()
                    print(f"{i} 삽입 성공")
                except:
                    print(f"{i} 삽입 실패")        
        else:
            session['ingredient']=ing
            
        cur.close()
        
        return redirect('/index')
    



@server.route('/mypage', methods=['GET', 'POST'])
def mypage():
    user_id = session['user_id']
    mydb = mysql_connetion()
    cur = mydb.cursor()
    
    # 관리할 재료 조회
    cur.execute(f"select ingredients, expiration_date from user_ingredients where id ='{user_id}';")
    ing_list = cur.fetchall()
    ing_li = list(map(lambda x: ing_list[x][0], range(len(ing_list))))
    ing_ex_li1 = list(map(lambda x: ing_list[x][1], range(len(ing_list))))
    now = datetime.datetime.now()
    ###남은 날짜 x
    ing_ex_li = []
    #y = []
    for i in range(len(ing_ex_li1)):
        lastdate = datetime.datetime.strptime(ing_ex_li1[i][:10],'%Y-%m-%d')
        ing_ex_li.append((lastdate - now).days)
        #y.append ( ( now-lastdate  ).days)
        
    # 남은 일수에 따른 색상
    ing_ex_color = []
    for x in range(len(ing_ex_li)):
        if ing_ex_li[x] <= 1:
            ing_ex_color.append('#ff4d4d;')
        elif ing_ex_li[x] <= 4:
            ing_ex_color.append('#ffed4d')
        else:
            ing_ex_color.append('#2feb3f')
    else:
        pass
            
    
    # 친구 조회
    cur.execute(f"select friend from user_friends where id = '{user_id}' AND accept = 1;")
    friends = cur.fetchall()
    friend_list = list(map(lambda x: friends[x][0], range(len(friends))))
    
    # 친구요청 메세지 조회
    friend_message = Recom1.friend_mesaage(f'{user_id}')
    print(friend_message)
    
    
    # 레시피 메세지 조회
    promise, senderid, sendersex,senderage,senderscoer,messages,myingruse,promisedate,priomisetime,recipenum,recipetitle,total_users2,promise_code = Recom1.kkan_recive_status(f'{user_id}')
    # promise # 메세지 넘버링용도
    # senderid # 보낸 사람 id
    # sendersex # 보낸 사람 성별
    # senderage # 보낸 사람 나이
    # senderscoer # 보낸 사람 점수
    # messages # 보낸 내용
    # myingruse # 내가 사용할 수 있는 재료
    # promisedate # 약속 날짜
    # priomisetime # 약속 시간
    # recipenum # 레시피 넘버
    # recipetitle # 레시피 제목
    # total_users2 # 같이 모이는 사람들
    # promise_code # 약속 고유 번호
    ############### 메세지 예상 ###############
    # 00세 남성인 kmr user님이 recipenumm을 제안했어요.
    # 날짜 시간 텍스트 
    # 재료:  
    # 약속코드
    
    
    ################### 약속관리에 뿌려줄 변수 (뒤에 2) 
    #같이 하는사람, 나이, 성별, 약속한날, 약속한 시간, 남은 날, 남은 시간, 내사용재료, 그룹사야될재료, 레시피번호, 레시피 타이틀
    kkanbu2,age2,sex2,promisedate2,promisetime2,remaindays2,remaintime2,myingr2,groupneed2,recipenum2,rectitle2 = Recom1.promise_list(user_id)
    ############### 메세지 예상 ###############
    
    
    ####### 유튜브 검색
    # 주소에 입력 안되는 값 제외 
    # rectitle2= ["고기처럼 쫄깃한 밥도둑 반찬 '새송이버섯 간장버터구이'레시피"]
    if rectitle2:
        no_q = '''@#$%^&*+='"[{]}\|;:,/?'''
        for x in range(len(rectitle2)):
            for s in range(len(no_q)):
                rectitle2[x] = rectitle2[x].replace(no_q[s],"")
            # 주소에서 띄어쓰기는 +형식
            rectitle2[x] = rectitle2[x].replace(" ",'+')
            
    cur.close()
    
    if session['mypage_message']:
        flash(session['mypage_message'])
        session['mypage_message'] = False
    
    return render_template("mypage.html", user=user_id, ing_li=ing_li, ing_ex_li=ing_ex_li, ing_ex_color=ing_ex_color, friend_list=friend_list, friend_message=friend_message, senderage=senderage, sendersex=sendersex, senderid=senderid, recipenum=recipenum, promisedate=promisedate, priomisetime=priomisetime, messages=messages, myingruse=myingruse, promise_code=promise_code, kkanbu2=kkanbu2,age2=age2,sex2=sex2,promisedate2=promisedate2,promisetime2=promisetime2,remaindays2=remaindays2,remaintime2=remaintime2,myingr2=myingr2,groupneed2=groupneed2,recipenum2=recipenum2,rectitle2=rectitle2)



# 친구 요청
@server.route('/sendmail', methods=['POST'])
def sendmail():
    
    if request.method == 'POST':  
    #####
        userid = request.form.get("id")
        reciever = request.form.get("receiver")
        Recom1.friend_request(userid,reciever)
        session['fri_propose'] = f'{reciever}님에게 친구요청을 보냈습니다.'

    return redirect("/index")


@server.route('/friend_accept', methods=['POST'])
def f_accept():
    user_id = session['user_id']
    
    if request.method == 'POST':
        friend = request.form.get('friend')
        accept = request.form.get('accept')
        
        try:
            Recom1.friend_accept(user_id, friend, accept)
            
            if accept == 'yes':
                session['mypage_message'] = f'{friend}님의 친구 요청을 수락했습니다.'
                print('친구 수락')
            else:
                session['mypage_message'] = f'{friend}님의 친구 요청을 거절했습니다.'
                print('친구 거절')
        except:
            print('깐부 요청 처리 오류')
    
    return redirect('/mypage')



@server.route('/friend_delete', methods=['POST'])
def f_delete():
    user_id = session['user_id']
    
    if request.method == 'POST':
        friend = request.form.get('friend')
        try:
            Recom1.friend_delete(user_id, friend)
        except:
            print('깐부 제거 처리 오류')
        
        session['mypage_message'] = f'{friend}님을 깐부 목록에서 제거했습니다.'
        print('깐부 제거')
        
    return redirect('/mypage')


# 추천받은 레시피 보기 페이지
@server.route('/result', methods=['POST'])
def result():
    user_id = session['user_id']
    users = [user_id]
    #users = ['kmr_user']
    if request.method == 'POST':
        title = request.form.get('recipe_title')
        num = request.form.get('recipe_num')
        img = request.form.get('recipe_img')
        fr = request.form.get('friend')
        
        # name=friend인 값(실제 친구들 or 추천 유저)가 존재하면 
        if fr:
            friends = list(map(lambda x : x[1:-1], (fr[1:-1]).split(", ")))
            for i in friends:
                users.append(i)
        else:
            print('친구 없음')
            friends = []
            pass
            
        ### users[0]: 나, users[1]: 친구 ..(이후도 다 친구)
        ## exingr는 각 유저별 쓰는거
        ## non 내가 갖고있는데 레시피에 안들어가는거
        ## group exist 는 그룹전체로 쓰게될 재료
        ## groupbuy는 그룹전체가 구매해야될 재료
        # num = 6899937
        try:
            exingr, nonexingr, groupexist, groupby = Recom1.ingr_exist(num,users)
            print(f'exingr: {exingr}')
            print(f'nonexingr: {nonexingr}')
            print(f'groupexist: {groupexist}')
            print(f'groupby: {groupby}')
        except:
            print('조회 안됨')
        return render_template("result.html", friends=friends, title=title, num=num, img=img, users=users, exingr=exingr, groupby=groupby)


# 레시피 메일 전송 페이지
@server.route('/mail', methods=['POST'])
def mailpage():
    user_id = session['user_id']
    
    if request.method == 'POST':
        today = datetime.datetime.today()
        today = today.strftime('%Y-%m-%d')
        title = request.form.get('title')
        num = request.form.get('num')
        img = request.form.get('img')
        friend = request.form.getlist('friend')
    return render_template("mail.html", user_id=user_id, title=title, num=num, img=img, friend=friend, today=today)


# 레시피 만들기 편지 전송
@server.route('/sendmail2', methods=['GET', 'POST'])
def sendmail2():
    if request.method == 'POST':
        sender = session['user_id']
        print(f'sender: {sender}')
        friendsid = request.form.getlist('friend')  ##list로생각하고 ["user1", "user2"] 
        print(f'recipien: {friendsid}')
        recipe = request.form.get('num')
        print(f'recipe: {recipe}')
        date = request.form.get('date')
        date = str(date)
        print(f'date: {date}')
        time = request.form.get('time')
        time = str(time)
        print(f'time: {time}')
        text = request.form.get('text')
        print(f'text: {text}')
        
        
        
        # sender = "kmr_user"
        # friendsid = ['kmr_friend2', 'kmr_friend3']
        # recipe = 6857486
        # date ="2022-01-20"
        # time = "16:00"
        # text = "진철집으로"
        
        
        reciver_score = Recom1.sender_rank(sender, friendsid)
        
        sender_score = []   
        for i in range(len( friendsid)) :
            sscore = Recom1.sender_rank( friendsid[i], [ sender ] )
            sender_score.append(sscore[0])
        
        ##메시지 전송
        now=datetime.datetime.now()
        nowDatetime = now.strftime('%Y%m%d-%H:%M:%S')  
        #cur.execute(f"select ingredients from user_ingredients where id ='{user_id}';")
        #ing_list = cur.fetchall()

        
        #약속코드 생성
        ##1번 약속코드
        promise_num = random_code()
        #date = nowDatetime
        ##테이블에 채워야 하는 정보를 끌어오는 함수
        sender, sender_age, sender_sex, sendertend, recipe_code,needingr,friends_id,friends_age,friends_sex,friends_tend= Recom1.kkanbuinfo(sender, friendsid,recipe)

        users = []
        users.append(sender)
        users = users + friendsid
        accept_date = '0'
        accept = '0'
        review ='0'
        
        exingr, nonexingr, groupexist, groupbuy = Recom1.ingr_exist(recipe,users)
        
        groupexist = ", ".join(groupexist)
        groupbuy = ", ".join(groupbuy)
        mydb = mysql_connetion()
        cur = mydb.cursor()  
        try:
            for i in range(len(users)):
                exingr[i] = ", ".join(exingr[i])
                if exingr[i] == "":
                    exingr[i] = "몸만오세요 사면됩니다"

                if i !=0:
    
                    cur.execute(f"INSERT INTO kkanbu(promise_num,date, sender, sender_age, sender_sex,sender_score, reciver, reciver_age, reciver_sex, reciver_score, recipe_num, recipe_code, sender_prefer,reciver_prefer, promise_date, promise_time, message, need_ingredients, user_ingredients, friend_ingredients, group_ingredients, buy_ingredients, accept_date, accept, review) VALUES('{promise_num}', '{nowDatetime}', '{sender}', '{sender_age}', '{sender_sex}','{sender_score[i-1]}', '{friends_id[i-1]}', '{friends_age[i-1]}','{friends_sex[i-1]}', '{reciver_score[i-1]}', '{recipe}', '{recipe_code}', '{sendertend}','{friends_tend[i-1]}', '{date}', '{time}',   '{text}', '{needingr}',   '{exingr[0]}', '{exingr[i]}' ,   '{groupexist}', '{groupbuy}', '{accept_date}' ,   '{accept}', '{review}');")
                    
                    mydb.commit()
                
                print('삽입 성공')
        except:
            print('삽입 실패') 
        
        cur.close()
        return redirect('/mypage')


@server.route('/recipe_accept', methods=['POST'])
def r_accept():
    user_id = session['user_id']

    if request.method == 'POST':
        sender = request.form.get('sender')
        promise_num = request.form.get('promise_num')
        accept = request.form.get('accept')
        
        
        session['mypage_message'] = True
        message = Recom1.kkanbu_accept(user_id,sender,promise_num,accept)
        session['mypage_message'] = message
        print(f'{message}')
        
    return redirect('/mypage')









if __name__ == "__main__":
    server.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False) 
