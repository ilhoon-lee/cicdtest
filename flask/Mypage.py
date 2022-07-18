# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:50:56 2022

@author: user
"""
import mysql.connector
import os
import random
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import string
import seaborn as sns
import boto3
import Kkanocr
import time

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

mydb = mysql.connector.connect(
    host="mysql.cbtzgcvtawc2.ap-northeast-2.rds.amazonaws.com",
    user="root",
    passwd="pass123#",
    database="recipe"
)

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
#friend_status("kmr_user")
def friend_status(userid):
    mydb = mysql_connetion()
    cur = mydb.cursor()


    try:
        cur.execute(f"select friend from user_friends where id = '{userid}' AND accept = 1;")
        friends = cur.fetchall()
        
        friend_list = list(map(lambda x: friends[x][0], range(len(friends))))
        print('친구 조회 성공')
    except:  
        friend_list = []
        print('친구 조회 실패')
        
    
    cur.close()    
    return friend_list


#friend_request("kmr_user","bohem")
##친구요청하기 일단 0으로 요청
def friend_request(userid,reciever):
    mydb = mysql_connetion()
    cur = mydb.cursor()
    now=datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')  
    accept = '0'

    #reciever = 'kmr_user'
    try:
        cur.execute(f"select id from user_info where id = '{reciever}';")
        existuser = cur.fetchall()

        try:
            # 아이디 확인
            cur.execute(f"INSERT INTO user_friends(id, friend, accept, date) VALUES( '{userid}', '{reciever}', '{accept}', '{nowDatetime}' );")
            mydb.commit()
            print(reciever+" 님께 깐부요청을 보냈습니다.")
        except:
            print("이미 친구요청중인 깐부입니다.")
            
    except:
        print("회원정보에 없는 유저입니다.")
    
    cur.close()




#friend_delete("kmr_user","bohem")
def friend_delete(userid,del_friend):
    #userid="kmr_user"
    mydb = mysql_connetion()
    cur = mydb.cursor()
    try:
        cur.execute(f"delete from user_friends where id = '{userid}' and friend = '{del_friend}' and accept = 1;")
        cur.execute(f"delete from user_friends where id = '{del_friend}' and friend = '{userid}' and accept = 1;")
        mydb.commit()  
        print('친구 삭제 성공')
    except:  
        print('친구 삭제 실패')
    cur = mydb.cursor()  
        
    cur.close()

#friend_accept("kmr_user","bohem","yes")
def friend_accept(userid,friend,accept):
    #userid="kmr_user"
    #del_friend = "bohem"
    mydb = mysql_connetion()
    cur = mydb.cursor()
    now=datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')  
    if accept == "yes":
        #수락의경우 userid 에서 0을 ->1로
        #reciver 를 userid로 accept를 1로

        try:
            cur.execute(f"UPDATE user_friends SET accept = '1' WHERE id = '{userid}' and friend = '{friend}' and accept = '0';")
            mydb.commit()
            
            cur.execute(f"INSERT INTO user_friends(id, friend, accept, date) VALUES( '{friend}', '{userid}', '1', '{nowDatetime}' );")
            mydb.commit()

            print('친구 수락 성공')
        except:  
            print('친구 수락 중 문제발생 ')
            
    elif accept == "no":
        try:
            cur.execute(f"delete from user_friends where id = '{userid}' and friend = '{friend}' and accept = '0';")
            mydb.commit()

            print('깐부요청 거절')
        except:  
            print('요청처리 실패')
    else:
        print("함수 입력값 오류")

    cur.close()
    
def friend_accept(userid,friend,accept):
    #userid="kmr_user"
    #del_friend = "bohem"
    mydb = mysql_connetion()
    cur = mydb.cursor()
    now=datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')  
    if accept == "yes":
        #수락의경우 userid 에서 0을 ->1로
        #reciver 를 userid로 accept를 1로

        try:
            cur.execute(f"UPDATE user_friends SET accept = '1' WHERE id = '{userid}' and friend = '{friend}' and accept = '0';")
            mydb.commit()
            
            cur.execute(f"INSERT INTO user_friends(id, friend, accept, date) VALUES( '{friend}', '{userid}', '1', '{nowDatetime}' );")
            mydb.commit()

            print('친구 수락 성공')
        except:  
            print('친구 수락 중 문제발생 ')
            
    elif accept == "no":
        try:
            cur.execute(f"delete from user_friends where id = '{userid}' and friend = '{friend}' and accept = '0';")
            mydb.commit()

            print('깐부요청 거절')
        except:  
            print('요청처리 실패')
    else:
        print("함수 입력값 오류")

    cur.close()
    
# user_id = "kmr_user"
# friendsid = ["kmr_friend","kmr_friend2"]
# recnum='6932754'
# kkanbuinfo(user_id, friendsid,recnum)
def kkanbuinfo(user_id, friendsid,recnum):
    mydb = mysql_connetion()
    cur = mydb.cursor()
    
    try:
        cur.execute(f"select * from user_info where id ='{user_id}';")
        myinfo = cur.fetchall()
        print("내정보 불러오기 완료")
        sender = myinfo[0][1]
        sender_age = myinfo[0][6]
        sender_sex = myinfo[0][7]
        sendertend = user_tend(user_id)
    except:
        print("user_info 쿼리에러")
    try:
        
        cur.execute(f"select * from recipe where number ='{recnum}';")
        recinfo = cur.fetchall()
        recipe_code = str( recinfo[0][2] )+str( recinfo[0][3] )+str( recinfo[0][4] )
        needingr = recinfo[0][5] 
        needingr.split("/")
        needingr = ', '.join(needingr.split("/"))
        print("함께할 레시피정보 불러오기 완료")
    except:
        print("user_info 쿼리에러")
    

    
    friends_id,friends_age,friends_sex,friends_tend = [],[],[],[]
    try:
        for i in range(len(friendsid)):
            cur.execute(f"select * from user_info where id ='{friendsid[i]}';")
            friendif = cur.fetchall()
            #friendsinfo.append(friendif)
            friends_id.append(friendif[0][1])
            friends_age.append(friendif[0][6])
            friends_sex.append(friendif[0][7])
            friends_tend.append(user_tend(friendsid[i]))
            
    except:
        print("user_info 쿼리에러")

    cur.close()
    return sender, sender_age, sender_sex,sendertend, recipe_code,needingr,friends_id,friends_age,friends_sex,friends_tend


def user_tend(user_id):
    cur = mydb.cursor()  
    
    try:
        cur.execute("SELECT * FROM user_select where id like '"+user_id+"' order by YMD desc;")
        usertend = cur.fetchall()
        xxdf = pd.DataFrame(usertend)
        # tend = pd.DataFrame([[0 for j in range(1,5)] for i in range(1,8)], index = [j for j in range(1,8)], columns = [j for j in range(1,5) ])
        #main_cook = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[5][x]), range(len(xxdf))))
        code_sum = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[4][x])+ str(xxdf[5][x]), range(len(xxdf))))
        
        # for i in range(len(main_cook)):
        #     tend[int(main_cook[i][0])][int(main_cook[i][1])] = tend[int(main_cook[i][0])][int(main_cook[i][1])] +1 
         
        code_sumdict = sorted(get_count(code_sum).items(), key = lambda item: item[1], reverse = True)

        # sel_main = {}
        # sel_cook = {}
        # for i in range(1,5):
        #     print(i," : ",tend[i].sum())
        #     sel_main[i] = tend[i].sum()                                  
        # topmain1 = max(sel_main,key=sel_main.get)
        # del sel_main[ max(sel_main,key=sel_main.get) ]
        # topmain2 = max(sel_main,key=sel_main.get)
    
        # for i in range(7):
        #     print(i+1," : ",tend.iloc[i].sum())
        #     sel_cook[i+1] = tend.iloc[i].sum()   
    
        # topcook1 =  max(sel_cook,key=sel_cook.get)
        # del sel_cook[ max(sel_cook,key=sel_cook.get) ]
        # topcook2 =  max(sel_cook,key=sel_cook.get)
        
        topcode1 = code_sumdict[0][0]
        #topcode2 = code_sumdict[1][0]
        
        
    except:
        print("user_select 쿼리중 에러발생 ")
    cur.close()
    
    return topcode1


def user_tend(user_id):
    cur = mydb.cursor()  
    
    try:
        cur.execute("SELECT * FROM user_select where id like '"+user_id+"' order by YMD desc;")
        usertend = cur.fetchall()
        xxdf = pd.DataFrame(usertend)
      
        code_sum = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[4][x])+ str(xxdf[5][x]), range(len(xxdf))))

        code_sumdict = sorted(get_count(code_sum).items(), key = lambda item: item[1], reverse = True)

        
        topcode1 = code_sumdict[0][0]

        
    except:
        print("user_select 쿼리중 에러발생 ")
    cur.close()
    
    return topcode1
