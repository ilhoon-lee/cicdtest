# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 22:33:36 2021

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


def make_queryand(find_value,table,where_list="",where_value="",where_likelist ="",where_likevalue = "",group="",order="",limit = ""):
    que1 = "SELECT " + find_value + " FROM " + table 

    if where_list != "":
        que1 = que1 + " WHERE"
        for i in range(len(where_list)):
            if i == 0:
                que1 = que1 + " " + where_list[i] + " = " + where_value[i] 
                
            else:
                que1 = que1 + " AND " + where_list[i] + " = " +  where_value[i]
                
    if where_likelist != "" and where_list == "":
        que1 = que1 + " WHERE"
        for i in range(len(where_likelist)):
            if i == 0:
                que1 = que1 + " " + where_likelist[i] + " like " + where_likevalue[i] 
                
            else:
                que1 = que1 + " AND " + where_likelist[i] + " like " +  where_likevalue[i] 

    elif where_likelist != "" and where_list != "":
        que1 = que1 + " AND"
        for i in range(len(where_likelist)):
            if i == 0:
                que1 = que1 + " " + where_likelist[i] + " like " +where_likevalue[i] 
                
            else:
                que1 = que1 + " AND " + where_likelist[i] + " like " +  where_likevalue[i] 
                
    if group !="":
        que1 = que1 + " GROUP BY " + group
    
    
    if order != "" and str(limit) != "":
        que1 = que1 + " ORDER BY " + order + " LIMIT " +str(limit)
    elif order != "" and str(limit) == "":
        que1 = que1 + " ORDER BY " + order    
        
    que1 = que1 + ";"        
    return(que1)

def make_queryor(find_value,table,where_list="",where_value="",where_likelist ="",where_likevalue = "",group="",order="",limit = ""):
    que1 = "SELECT " + find_value + " FROM " + table 

    if where_list != "":
        que1 = que1 + " WHERE"
        for i in range(len(where_list)):
            if i == 0:
                que1 = que1 + " " + where_list[i] + " = " + where_value[i] 
                
            else:
                que1 = que1 + " AND " + where_list[i] + " = " +  where_value[i]
                
    if where_likelist != "" and where_list == "":
        que1 = que1 + " WHERE"
        for i in range(len(where_likelist)):
            if i == 0:
                que1 = que1 + " " + where_likelist[i] + " like " + where_likevalue[i] 
                
            else:
                que1 = que1 + " OR " + where_likelist[i] + " like " +  where_likevalue[i] 

    elif where_likelist != "" and where_list != "":
        que1 = que1 + " AND"
        for i in range(len(where_likelist)):
            if i == 0:
                que1 = que1 + " " + where_likelist[i] + " like " +where_likevalue[i] 
                
            else:
                que1 = que1 + " OR " + where_likelist[i] + " like " +  where_likevalue[i] 
                
    if group !="":
        que1 = que1 + " GROUP BY " + group
    
    
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

def user_info(userid):
    mydb = mysql.connector.connect(
        host="mysql.cbtzgcvtawc2.ap-northeast-2.rds.amazonaws.com",
        user="root",
        passwd="pass123#",
        database="recipe"
        )
    ########테스트 후 삭제하거나 주석처리할것
    #userid = 'kmr_user'
 
    
    cur = mydb.cursor()  
    cur.execute("SELECT * FROM user_select where id like '"+userid+"' order by YMD desc;")
    usertend = cur.fetchall()
    cur.execute("SELECT * FROM user_ingredients where id like '"+userid+"';")
    ingr_temp = cur.fetchall()
    
    #ingr_temp[0][4]
    #######
    user_ingr = list(map(lambda x : ingr_temp[x][1], range(len(ingr_temp))))
    user_ingrnum = list(map(lambda x : ingr_temp[x][4], range(len(ingr_temp))))
    mainingr = ""
    where_list = []
    where_value = []
    where_likelist = []
    where_likevalue = []
    
    for i in range(len(user_ingr)):
        if user_ingr[i] in "소고기":
            mainingr = "1"
            where_value.append(mainingr)
            where_list.append("code_main")
        elif user_ingr[i] in "돼지고기":
            mainingr = "2"
            where_value.append(mainingr)
            where_list.append("code_main")
        elif user_ingr[i] in "닭고기":
            mainingr = "3"
            where_value.append(mainingr)
            where_list.append("code_main")
        elif user_ingr[i] in ["해산물","전복","오징어","갈치","연어"]:
            mainingr = "4"
            where_value.append(mainingr)
            where_list.append("code_main")
        else: 
            where_likevalue.append("'%" + user_ingr[i]+ "%'")
            where_likelist.append("ingredients")
            
    
    xxdf = pd.DataFrame(usertend)
    tend = pd.DataFrame([[0 for j in range(1,5)] for i in range(1,8)], index = [j for j in range(1,8)], columns = [j for j in range(1,5) ])
    main_cook = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[5][x]), range(len(xxdf))))
    code_sum = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[4][x])+ str(xxdf[5][x]), range(len(xxdf))))
    
    for i in range(len(main_cook)):
        tend[int(main_cook[i][0])][int(main_cook[i][1])] = tend[int(main_cook[i][0])][int(main_cook[i][1])] +1 
     
    code_sumdict = sorted(get_count(code_sum).items(), key = lambda item: item[1], reverse = True)
    

    if mainingr == "":
        print("no main ingr")
        ###메인재료 1등, 조리법 1등 - 2개, 조리법 2등 2개
        ### 메인재료 2등 조리법 1등 2개 조리법 2등 2개
        ###2개는 top5 select에서
        
        orderval = "code_cook"
        len(where_likevalue)
        where_likelist[0]  = "(" + where_likelist[0]
        where_likevalue[len(where_likevalue) -1 ]  = where_likevalue[-1][:-1] + "')"

        sel_main = {}
        sel_cook = {}
        for i in range(1,5):
            print(i," : ",tend[i].sum())
            sel_main[i] = tend[i].sum()                                  
        topmain1 = max(sel_main,key=sel_main.get)
        del sel_main[ max(sel_main,key=sel_main.get) ]
        topmain2 = max(sel_main,key=sel_main.get)

        for i in range(7):
            print(i+1," : ",tend.iloc[i].sum())
            sel_cook[i+1] = tend.iloc[i].sum()   

        topcook1 =  max(sel_cook,key=sel_cook.get)
        del sel_cook[ max(sel_cook,key=sel_cook.get) ]
        topcook2 =  max(sel_cook,key=sel_cook.get)
        
        topcode1 = code_sumdict[0][0]
        topcode2 = code_sumdict[1][0]
    ############################3    
        # cur = mydb.cursor() 
        # cur.execute( make_query("code_cook,count(*)","recipe","","",where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
        # and_val = cur.fetchall()
        
        # cur.execute( make_queryor("code_cook,count(*)","recipe","","",where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
        # or_val = cur.fetchall()    

        user_rec = []
        where_list11 = [["code_main","code_cook"],["code_main","code_cook"],["code_main","code_cook"],["code_main","code_cook"],["code_main","code_sub","code_cook"],["code_main","code_sub","code_cook"]]
        where_value11 = [[str(topmain1),str(topcook1)],[str(topmain1),str(topcook2)],[str(topmain2),str(topcook1)],[str(topmain2),str(topcook2)],[topcode1[0],topcode1[1],topcode1[2]],[topcode2[0],topcode2[1],topcode2[2]]]
        lim = [2,2,2,2,1,1]
        for i in range(len(where_list11)):
            cur.execute(make_queryand("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i] ) )
            res = cur.fetchall()
            if len(res) ==lim[i] and res != []:
                user_rec.append(res)    
            elif len(res) == lim[i]-1 and res != []:
                cur.execute(make_queryand("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i]) )
                user_rec.append(res)
                cur.execute(make_queryor("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i]) ) 
                res = cur.fetchall()
                user_rec.append(res)
            else:
                cur.execute(make_queryor("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i]) ) 
                res = cur.fetchall()
                user_rec.append(res)

        len(user_rec)
        user_rec = sum(user_rec, [])

        random.shuffle(user_rec)
            
            
        return user_rec
##################################################################################3

####################################메인재료 있을때,         
    else:  
        #########################재료뽑기 가중치 주기 #########
        user_cook1,user_cook2 = {},{}
        for i in range(len(code_sumdict)):
            if code_sumdict[i][0][0] == mainingr:
                print(code_sumdict[i][0])
                #user_cook.append(code_sumdict[i][0][2])
                user_cook1[int( code_sumdict[i][0][2] ) ] = code_sumdict[i][1]   
                
            elif code_sumdict[i][0][0] != mainingr:  
                user_cook2[int( code_sumdict[i][0][2] ) ] = code_sumdict[i][1]
            
            
        key1 = list(user_cook1.keys())
        val1 = list(user_cook1.values())
        
        key2 = list(user_cook2.keys())
        val2 = list(user_cook2.values())
        
        
        ################################################################
        
        ###################### 뽑을 레시피 번호######################3
        q_val = [0,0,0,0,0,0,0,0]
        
        for i in range(len(user_cook1)):
            q_val[key1[i]] = q_val[key1[i]] + val1[i] * 3
            #q_val[0] = q_val[0] +1
        #user_cook1 에서 해결
        for i in range(len(user_cook2)):
            q_val[key2[i]] = q_val[key2[i]] + val2[i]
            
        q_val2 = list(map(lambda x : int( round( q_val[x]*10/sum(q_val),0) ) ,range(len(q_val))))
        sum(q_val2)

        while sum(q_val2) !=10:
            
            if sum(q_val2) > 10:
                q_val2[ q_val2.index( max(q_val2) ) ] = q_val2[ q_val2.index( max(q_val2) ) ]-1
            elif sum(q_val2) < 10:
                q_val2[ q_val2.index( max(q_val2) ) ] = q_val2[ q_val2.index( max(q_val2) ) ]+1
                
        ######################################재료가 들어간 레시피의 개수 확인#######  
        ##sum(q_val2)

        orderval = "code_cook"
        len(where_likevalue)
        where_likelist[0]  = "(" + where_likelist[0]
        where_likevalue[len(where_likevalue) -1 ]  = where_likevalue[1][:-1] + "')"
        cur = mydb.cursor() 
        cur.execute( make_queryand("code_cook,count(*)","recipe",where_list,where_value,where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
        and_val = cur.fetchall()
        
        cur.execute( make_queryor("code_cook,count(*)","recipe",where_list,where_value,where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
        or_val = cur.fetchall()
        
        ############################################################################
        user_rec =[]
        where_list1 = []
        where_value1 = []
        
        and_val1 = [0,0,0,0,0,0,0,0]
        or_val1 = [0,0,0,0,0,0,0,0]
        for i in range(len(and_val)):
            and_val1[and_val[i][0]] = and_val1[and_val[i][0]] + and_val[i][1]
            
        for i in range(len(or_val)):
            or_val1[or_val[i][0]] = or_val1[or_val[i][0]] + or_val[i][1]
           
            
        for i in range(len(q_val2)):
            if q_val2[i] != 0 and q_val2[i] <= or_val1[i] + and_val1[i]:
                if and_val1[i] >= q_val2[i] :
                    where_list1 = ["code_main","code_cook"]
                    where_value1.append( mainingr ) 
                    where_value1.append( str(i) )
                    cur.execute(make_queryand("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i]) )
                    res = cur.fetchall()
                    user_rec.append(res)
                    where_list1 = []
                    where_value1 = []
                    
                elif and_val1[i] !=0 and and_val1[i] < q_val2[i] and q_val2[i]<or_val1[i] :
                
                    where_list1 = ["code_main","code_cook"]
                    where_value1.append( mainingr ) 
                    where_value1.append( str(i) )
                    cur.execute(make_queryand("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=and_val1[i]) )
                    res = cur.fetchall()
                    user_rec.append(res)
                    cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i] - and_val1[i]) )
                    res = cur.fetchall()
                    user_rec.append(res)
                    where_list1 = []
                    where_value1 = []     
                elif and_val1[i] ==0 and q_val2[i]<or_val1[i]:
                    where_list1 = ["code_main","code_cook"]
                    where_value1.append( mainingr ) 
                    where_value1.append( str(i) )
                    cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i]) )
                    res = cur.fetchall()
                    user_rec.append(res)
                    where_list1 = []
                    where_value1 = []   
                elif and_val1[i] ==0 and q_val2[i] > or_val1[i]:
                    where_list1 = ["code_main","code_cook"]
                    where_value1.append( mainingr ) 
                    where_value1.append( str(i) )
                    cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=or_val1[i]) )
                    res = cur.fetchall()
                    user_rec.append(res)
                    where_list1 = []
                    where_value1 = []  
                    
                    where_list1 = ["code_main"]
                    where_value1.append( mainingr ) 
                    cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i] - or_val1[i]) )
                    res = cur.fetchall()
                    user_rec.append(res)
                    where_list1 = []
                    where_value1 = []  
                    
        user_rec = sum(user_rec, [])
        random.shuffle(user_rec)
        len(user_rec)
        return user_rec


# users = ["kmr_user",'bohem']
# user_match(users)
def user_match(users):
    
    #users = ["kmr_user","kmr_friend","kmr_friend2"]
    
    #len(users)
    
    mydb = mysql.connector.connect(
        host="mysql.cbtzgcvtawc2.ap-northeast-2.rds.amazonaws.com",
        user="root",
        passwd="pass123#",
        database="recipe"
        )
    ########  
    
    #i=0
    ingr_users = []
    tend_users = []
    
    for i in range(len(users)):

        cur = mydb.cursor()  
        cur.execute("SELECT * FROM user_select where id like '"+users[i]+"' order by YMD desc;")
        usertend = cur.fetchall()
        tend_users.append(usertend)
        cur.execute("SELECT * FROM user_ingredients where id like '"+users[i]+"';")
        ingr_temp = cur.fetchall()
        ingr_users.append(ingr_temp)
    #######
    
        sum_ingr = sum(ingr_users, [])
        user_ingr = list(map(lambda x : sum_ingr[x][1], range(len(sum_ingr))))
    #userid2 = "kmr_friend"

    sum_ingr = list (set(user_ingr) )
    mainingr = []
    where_list = []
    where_value = []
    where_likelist = []
    where_likevalue = []
    
    for i in range(len(sum_ingr)):
        if sum_ingr[i] in "소고기":
            mainingr.append("1")
            where_value.append(mainingr)
            where_list.append("code_main")
        elif sum_ingr[i] in "돼지고기":
            mainingr.append("2")
            where_value.append(mainingr)
            where_list.append("code_main")
        elif sum_ingr[i] in "닭고기":
            mainingr.append("3")
            where_value.append(mainingr)
            where_list.append("code_main")
        elif sum_ingr[i] in ["해산물","전복","오징어","갈치","연어"]:
            mainingr.append("4")
            where_value.append(mainingr)
            where_list.append("code_main")
        else: 
            where_likevalue.append("'%" + sum_ingr[i]+ "%'")
            where_likelist.append("ingredients")
            
    
    xxdf = pd.DataFrame(tend_users[0])
    tend = pd.DataFrame([[0 for j in range(1,5)] for i in range(1,8)], index = [j for j in range(1,8)], columns = [j for j in range(1,5) ])
    main_cook = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[5][x]), range(len(xxdf))))
    code_sum = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[4][x])+ str(xxdf[5][x]), range(len(xxdf))))
    
    for i in range(len(main_cook)):
        tend[int(main_cook[i][0])][int(main_cook[i][1])] = tend[int(main_cook[i][0])][int(main_cook[i][1])] +1 
     
    code_sumdict = sorted(get_count(code_sum).items(), key = lambda item: item[1], reverse = True)
    
    if mainingr == []:
        print("no main ingr")
        ###메인재료 1등, 조리법 1등 - 2개, 조리법 2등 2개
        ### 메인재료 2등 조리법 1등 2개 조리법 2등 2개
        ###2개는 top5 select에서
        
        orderval = "code_cook"
        len(where_likevalue)
        where_likelist[0]  = "(" + where_likelist[0]
        where_likevalue[len(where_likevalue) -1 ]  = where_likevalue[-1][:-1] + "')"

        sel_main = {}
        sel_cook = {}
        for i in range(1,5):
            #print(i," : ",tend[i].sum())
            sel_main[i] = tend[i].sum()                                  
        topmain1 = max(sel_main,key=sel_main.get)
        del sel_main[ max(sel_main,key=sel_main.get) ]
        topmain2 = max(sel_main,key=sel_main.get)

        for i in range(7):
            #print(i+1," : ",tend.iloc[i].sum())
            sel_cook[i+1] = tend.iloc[i].sum()   

        topcook1 =  max(sel_cook,key=sel_cook.get)
        del sel_cook[ max(sel_cook,key=sel_cook.get) ]
        topcook2 =  max(sel_cook,key=sel_cook.get)
        
        topcode1 = code_sumdict[0][0]
        topcode2 = code_sumdict[1][0]
        
        # cur = mydb.cursor() 
        # cur.execute( make_query("code_cook,count(*)","recipe","","",where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
        # and_val = cur.fetchall()
        
        # cur.execute( make_queryor("code_cook,count(*)","recipe","","",where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
        # or_val = cur.fetchall()        
        
        where_list11 = [["code_main","code_cook"],["code_main","code_cook"],["code_main","code_cook"],["code_main","code_cook"],["code_main","code_sub","code_cook"],["code_main","code_sub","code_cook"]]
        where_value11 = [[str(topmain1),str(topcook1)],[str(topmain1),str(topcook2)],[str(topmain2),str(topcook1)],[str(topmain2),str(topcook2)],[topcode1[0],topcode1[1],topcode1[2]],[topcode2[0],topcode2[1],topcode2[2]]]
        lim = [2,2,2,2,1,1]
        user_rec = []
        
        for i in range(len(where_list11)):
            cur.execute(make_queryand("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i] ) )
            res = cur.fetchall()
            if len(res) ==lim[i] and res != []:
                user_rec.append(res)    
            elif len(res) == lim[i]-1 and res != []:
                cur.execute(make_queryand("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i]) )
                user_rec.append(res)
                cur.execute(make_queryor("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i]) ) 
                res = cur.fetchall()
                user_rec.append(res)
            else:
                cur.execute(make_queryor("*","recipe",where_list11[i],where_value11[i],where_likelist,where_likevalue,group="",order="rand()",limit=lim[i]) ) 
                res = cur.fetchall()
                user_rec.append(res)

            
        user_rec = sum(user_rec, [])
        random.shuffle(user_rec)

        return user_rec

        
    else:  
        len(where_likevalue)
        where_likelist[0]  = "(" + where_likelist[0]
        where_likevalue[len(where_likevalue) -1 ]  = where_likevalue[-1][:-1] + "')"
        user_rec =[]
        
        if len(mainingr) ==1:
            kval = 10
        else:
            kval =5
        

        for k in range(len(mainingr)):
            #########################재료뽑기 가중치 주기 #########
            
            user_cook1,user_cook2 = {},{}
            for i in range(len(code_sumdict)):
                if code_sumdict[i][0][0] == mainingr[k]:
                    print(code_sumdict[i][0])

                    #user_cook.append(code_sumdict[i][0][2])
                    user_cook1[int( code_sumdict[i][0][2] ) ] = code_sumdict[i][1]   
                    
                elif code_sumdict[i][0][0] != mainingr[k]:  
                    user_cook2[int( code_sumdict[i][0][2] ) ] = code_sumdict[i][1]
                    print(code_sumdict[i][0])

            key1 = list(user_cook1.keys())
            val1 = list(user_cook1.values())
            
            key2 = list(user_cook2.keys())
            val2 = list(user_cook2.values())

            ################################################################
            
            ###################### 뽑을 레시피 번호######################3
            q_val = [0,0,0,0,0,0,0,0]
            
            for i in range(len(user_cook1)):
                q_val[key1[i]] = q_val[key1[i]] + val1[i] * 3
                #q_val[0] = q_val[0] +1
            #user_cook1 에서 해결
            for i in range(len(user_cook2)):
                q_val[key2[i]] = q_val[key2[i]] + val2[i]
                
            q_val2 = list(map(lambda x : int( round( q_val[x]*5/sum(q_val),0) ) ,range(len(q_val))))

            while sum(q_val2) !=kval:
                
                if sum(q_val2) > kval:
                    q_val2[ q_val2.index( max(q_val2) ) ] = q_val2[ q_val2.index( max(q_val2) ) ]-1
                elif sum(q_val2) < kval:
                    q_val2[ q_val2.index( max(q_val2) ) ] = q_val2[ q_val2.index( max(q_val2) ) ]+1
                
            ######################################재료가 들어간 레시피의 개수 확인#######  
            ##sum(q_val2)

            orderval = "code_cook"
            where_list = ["code_main"]
            where_value=[]
            where_value.append(mainingr[k])

            cur = mydb.cursor() 
            cur.execute( make_queryand("code_cook,count(*)","recipe",where_list,where_value,where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
            and_val = cur.fetchall()
            
            cur.execute( make_queryor("code_cook,count(*)","recipe",where_list,where_value,where_likelist,where_likevalue,group="code_cook",order=orderval,limit="") )
            or_val = cur.fetchall()
            
            ############################################################################
            
            where_list1 = []
            where_value1 = []
            
            and_val1 = [0,0,0,0,0,0,0,0]
            or_val1 = [0,0,0,0,0,0,0,0]
            for i in range(len(and_val)):
                and_val1[and_val[i][0]] = and_val1[and_val[i][0]] + and_val[i][1]
                
            for i in range(len(or_val)):
                or_val1[or_val[i][0]] = or_val1[or_val[i][0]] + or_val[i][1]
               
                
            for i in range(len(q_val2)):
                if q_val2[i] != 0 and q_val2[i] <= or_val1[i] + and_val1[i]:
                    if and_val1[i] >= q_val2[i] :
                        where_list1 = ["code_main","code_cook"]
                        where_value1.append( mainingr[k] ) 
                        where_value1.append( str(i) )
                        cur.execute(make_queryand("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i]) )
                        res = cur.fetchall()
                        user_rec.append(res)
                        where_list1 = []
                        where_value1 = []
                        
                    elif and_val1[i] !=0 and and_val1[i] < q_val2[i] and q_val2[i]<or_val1[i] :
                    
                        where_list1 = ["code_main","code_cook"]
                        where_value1.append( mainingr[k] ) 
                        where_value1.append( str(i) )
                        cur.execute(make_queryand("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=and_val1[i]) )
                        res = cur.fetchall()
                        user_rec.append(res)
                        cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i] - and_val1[i]) )
                        res = cur.fetchall()
                        user_rec.append(res)
                        where_list1 = []
                        where_value1 = []     
                    elif and_val1[i] ==0 and q_val2[i]<or_val1[i]:
                        where_list1 = ["code_main","code_cook"]
                        where_value1.append( mainingr[k] ) 
                        where_value1.append( str(i) )
                        cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i]) )
                        res = cur.fetchall()
                        user_rec.append(res)
                        where_list1 = []
                        where_value1 = []   
                    elif and_val1[i] ==0 and q_val2[i] > or_val1[i]:
                        where_list1 = ["code_main","code_cook"]
                        where_value1.append( mainingr[k] ) 
                        where_value1.append( str(i) )
                        cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=or_val1[i]) )
                        res = cur.fetchall()
                        user_rec.append(res)
                        where_list1 = []
                        where_value1 = []  
                        
                        where_list1 = ["code_main"]
                        where_value1.append( mainingr[k] ) 
                        cur.execute(make_queryor("*","recipe",where_list1,where_value1,where_likelist,where_likevalue,group="",order="rand()",limit=q_val2[i] - or_val1[i]) )
                        res = cur.fetchall()
                        user_rec.append(res)
                        where_list1 = []
                        where_value1 = []  
                        
        user_rec = sum(user_rec, [])
        

        random.shuffle(user_rec)

        return user_rec
    

def User_ingr_Score(user_id):
    cur = mydb.cursor()
    cur.execute("SELECT * FROM user_ingredients where id like '"+user_id+"';") #음식 재료 DB에서 출력
    ingr_temp = cur.fetchall()
    type(ingr_temp)
    #######
    user_ingr = list(map(lambda x : ingr_temp[x][1], range(len(ingr_temp)))) # 음식재료 리스트로 변환 
    
    cur.execute("SELECT * FROM ingredients ")
    food_ingredients_temp = cur.fetchall()

    ingdf = pd.DataFrame(food_ingredients_temp)                 
    
    xx = list(map(lambda x: ingdf[ingdf[0] == x  ], range(10) ))
    xx[1]
    xx = x[ x[0] ==1 ] # 주재료1 소고기 돼지고기 닭고기
    xx2 = x[x[0]==2 ] # 주재료2 해산물
    lisx1 = list(xx[1]) + list(xx2[1])
    xx3 = x[x[0]==8] #향신료 8
    xx4 = x[x[0]==9] #소스 9
    lisx2 = list(xx3[1]) + list(xx4[1])
    user_ingr

    #####################################기본  matching_score######################
    My_matching_score=0  # 나의 매칭 스코어
    for i in range(len(user_ingr)):
        if user_ingr[i] in lisx1:
            print("자신의 메인재료 +10점 ",user_ingr[i])
            My_matching_score+=10
            print(My_matching_score)
        elif user_ingr[i] in lisx2:
            print("자신의 조미료 +0점", user_ingr[i])
            print(My_matching_score)
        else:
            print("자신의 부재료 +1", user_ingr[i])
            My_matching_score+=1
            print(My_matching_score)
    My_matching_score

"""
Created on Mon Jan 10 16:40:42 2022

@author: user
"""
def unknown_info(user_ingr):
    mydb = mysql.connector.connect(
        host="mysql.cbtzgcvtawc2.ap-northeast-2.rds.amazonaws.com",
        user="root",
        passwd="pass123#",
        database="recipe"
        )

    cur = mydb.cursor()
    mainingr = ""
    where_list = []
    where_value = []
    where_likelist = []
    where_likevalue = []
    
    for i in range(len(user_ingr)):
        if user_ingr[i] in "소고기":
            mainingr = "1"
            where_value.append(mainingr)
            where_list.append("code_main")
        elif user_ingr[i] in "돼지고기":
            mainingr = "2"
            where_value.append(mainingr)
            where_list.append("code_main")
        elif user_ingr[i] in "닭고기":
            mainingr = "3"
            where_value.append(mainingr)
            where_list.append("code_main")
        elif user_ingr[i] in ["해산물","전복","오징어","갈치","연어"]:
            mainingr = "4"
            where_value.append(mainingr)
            where_list.append("code_main")
        else: 
            where_likevalue.append("'%" + user_ingr[i]+ "%'")
            where_likelist.append("ingredients")


    if mainingr == "":

        user_rec = []
        
        ### AND 로 재료 다들어가는거 10개있나 확인
        cur.execute(make_queryand("*","recipe","","",where_likelist,where_likevalue,group="",order="rand()",limit=10 ) )
        res = cur.fetchall()
        len(res)
        
        ## 10개가 안되면
        if len(res) == 10 and res != []:
            user_rec.append(res)    
        elif 0< len(res) < 10 and res != []:
            cur.execute(make_queryand("*","recipe","","",where_likelist,where_likevalue,group="",order="rand()",limit = len(res)) )
            res = cur.fetchall()
            user_rec.append(res)
            
            cur.execute(make_queryor("*","recipe","","",where_likelist,where_likevalue,group="",order="rand()",limit = 10 - len(res)) ) 
            res = cur.fetchall()
            user_rec.append(res)
        elif len(res) == 0:
            cur.execute(make_queryor("*","recipe","","",where_likelist,where_likevalue,group="",order="rand()",limit = 10) ) 
            res = cur.fetchall()
            user_rec.append(res)
            
        user_rec = sum(user_rec, [])
        random.shuffle(user_rec)
        
        
        return user_rec

    elif mainingr != "":
        len(where_likevalue)
        where_likelist[0]  = "(" + where_likelist[0]
        where_likevalue[len(where_likevalue) -1 ]  = where_likevalue[-1][:-1] + "')"    
    
        user_rec = []
        
        ### AND 로 재료 다들어가는거 10개있나 확인
        cur.execute(make_queryand("*","recipe",where_list,where_value,where_likelist,where_likevalue,group="",order="rand()",limit=10 ) )
        res = cur.fetchall()
        len(res)
        
        ## 10개가 안되면
        if len(res) == 10 and res != []:
            user_rec.append(res)    
        elif 0< len(res) < 10 and res != []:
            cur.execute(make_queryand("*","recipe",where_list,where_value,where_likelist,where_likevalue,group="",order="rand()",limit = len(res)) )
            res = cur.fetchall()
            user_rec.append(res)
            
            cur.execute(make_queryor("*","recipe",where_list,where_value,where_likelist,where_likevalue,group="",order="rand()",limit = 10 - len(res)) ) 
            res = cur.fetchall()
            user_rec.append(res)
        elif len(res) == 0:
            cur.execute(make_queryor("*","recipe",where_list,where_value,where_likelist,where_likevalue,group="",order="rand()",limit = 10) ) 
            res = cur.fetchall()
            user_rec.append(res)
            
        user_rec = sum(user_rec, [])
        random.shuffle(user_rec)

        return user_rec

def ingr_exist(recipenum,users):   
    
    mydb = mysql_connetion()
    cur = mydb.cursor()
    # 레시피 재료 조회
   #recipenum=6854871
    #users = ["kmr_user","kmr_friend"]
    cur.execute(f"select * from recipe where number ='{recipenum}';")
    recipe_ing = cur.fetchall()  
    recipe_main = recipe_ing[0][2]
    recipe_sub = recipe_ing[0][3]
    recipe_cook = recipe_ing[0][4]
    
    recipe_ingr = recipe_ing[0][5]
    recipe_ing_li = recipe_ingr.split('/')
    
    recipe_ingrnum = recipe_ing[0][6]
    recipe_ingnum_li = recipe_ingrnum.split('/')
    
    #str_recipe_ing = ', '.join(recipe_ing_li)
    
    if recipe_main == 1:
        recipe_ing_li[ recipe_ingnum_li.index("1") ] = "소고기" #+ recipe_ing_li[ recipe_ingnum_li.index("1") ] +">"
    elif recipe_main == 2:
        recipe_ing_li[ recipe_ingnum_li.index("1") ] = "돼지고기"#+ recipe_ing_li[ recipe_ingnum_li.index("2") ] +">"
    elif recipe_main == 2:
        recipe_ing_li[ recipe_ingnum_li.index("1") ] = "닭고기"#+ recipe_ing_li[ recipe_ingnum_li.index("3") ] +">"        
    elif recipe_main == 4 and recipe_sub == 1:
        recipe_ing_li[ recipe_ingnum_li.index("2") ] = "갈치"#+ recipe_ing_li[ recipe_ingnum_li.index("3") ] +">"         
    elif recipe_main == 4 and recipe_sub == 2:
        recipe_ing_li[ recipe_ingnum_li.index("2") ] = "연어"#+ recipe_ing_li[ recipe_ingnum_li.index("3") ] +">"      
    elif recipe_main == 4 and recipe_sub == 3:
        recipe_ing_li[ recipe_ingnum_li.index("2") ] = "오징어"#+ recipe_ing_li[ recipe_ingnum_li.index("3") ] +">"      
    elif recipe_main == 4 and recipe_sub == 4:
        recipe_ing_li[ recipe_ingnum_li.index("2") ] = "전복"#+ recipe_ing_li[ recipe_ingnum_li.index("3") ] +">"      

    # 유저들의 가진 재료 조회
    usersingr= []
    for i in range(len(users)):
        cur.execute(f"select * from user_ingredients where id ='{users[i]}';")
        ing_list = cur.fetchall()
        usersingr.append(ing_list)        
        
    exingr = []
    nonexingr = []
    needtobuy = []
    # 현재 레시피에서 내가 쓸 수 있는 재료 리스트
    for i in range(len(usersingr)):
        t_exingr = []
        t_nonexingr = []
        for j in range(len(usersingr[i])):
            if usersingr[i][j][1] in recipe_ing_li:
                t_exingr.append(usersingr[i][j][1])  
            else:# usersingr[j] not in recipe_ing_li: 
                t_nonexingr.append(usersingr[i][j][1])
                
        exingr.append(t_exingr)
        nonexingr.append(t_nonexingr)
        
    str_exing = []
    str_nonexing = []
    
    exingr1 = sum( exingr, [])
    nonexingr1 = sum( nonexingr, [])
    
    group_exing = list ( set( exingr1 ) & set(recipe_ing_li) ) 
    group_nonexing = list ( set(exingr1 ) ^ set(recipe_ing_li) ) 

    # 내 재료 텍스트로 바꾸기
    for i in range(len(exingr)):
        tmp_ing = ''
        tmp_ing = ', '.join(exingr[i])
        str_exing.append(tmp_ing)
        
        tmp_ing = ''
        tmp_ing = ', '.join(nonexingr[i])
        str_nonexing.append(tmp_ing)

    cur.close()
    
    return exingr, nonexingr, group_exing, group_nonexing

   # recipenum=6854871
   # users = ["kmr_user","kmr_friend","kmr_friend2"]
   # ingr_exist(recipenum,users)



#Matching_Score("kmr-user","kmr_friend")
def yoloresult(aws_save_name, container_path ):
    
    s3 = s3_connection()
    
    ###여기지우기
    #aws_save_name =  'leeilhoon123_20220112134431.jpg'
    #aws_save_name = 'gazi.txt'
    #container_path = 'C:/Users/user/Desktop/result/'
    #c_path = ''
    
    txtname = aws_save_name[:-4] + ".txt"
    bucket = 'user-test3467'
    object_name = 'txtresult/' + txtname
    
    ##### 경로 잘 지정할 것
    c_path =  container_path + txtname
    num = 1
    wait = ""
    while num != 10:
        try:
            s3.download_file(bucket, object_name, c_path) #    
            num = 10
        except Exception as e:
            time.sleep(0.5)
            wait  = wait +'-'
            print("waiting" + wait)
            
    try: 
        res_txt1 = pd.read_csv(c_path,sep=" ",header=None)
        res = yolov5result(res_txt1)
        keyls = list( res.keys() )
        valuels =list(res.values())
        return keyls, valuels
    except:
        return None, None

    
    

    
def yolov5result(res_txt):
    label = {0:"감자",1:"토마토",2:"애호박",3:"양파",4:"무",5:"가지",6:"대파",7:"적양배추",8:"당근",9:"계란",10:"소고기",11:"돼지고기",12:"닭고기"}
    retlist = []
    for i in range(len(res_txt)):
        #print(label[b[0][i]])
        retlist.append(label[res_txt[0][i]])
        
    return(get_occurrence_count(retlist))

def get_occurrence_count(my_list):
    new_list = {}
    for i in my_list:
        try: new_list[i] += 1
        except: new_list[i] = 1
        
    return(new_list)




def user_score(user):
    mydb=mysql_connetion()
    cur = mydb.cursor()
    #user = "kmr_friend2"
    #friend_id = "kmr_friend"
    #user = "Neptune"
    # user의 재료 검색
    #user = 'kmr_user'
    cur.execute("SELECT * FROM user_ingredients where id like '"+user+"';") #음식 재료 DB에서 출력
    ingr_temp = cur.fetchall()
    #######
    if ingr_temp != []:
    #user_ingr = list(map(lambda x: ingr_temp[x][0],range(len(ingr_temp)))) # 음식재료 리스트로 변환

    #####################################기본  matching_score######################
        matching_score=0  # 
        main_score = 0
        sub_score = 0
        extra_score = 0
        
        for i in range(len(ingr_temp)):
            if ingr_temp[i][4] == 1 or ingr_temp[i][4] == 2:
                if main_score ==0:
                    main_score = main_score + 20
                    #print("자신의 메인재료 +10점 ",user_ingr[i])
                elif main_score == 20:
                    main_score = 30
      
            elif ingr_temp[i][4] == 8 or ingr_temp[i][4] == 9:
                if extra_score ==0:
                    extra_score = extra_score + 5
                elif extra_score > 5:
                    extra_score = extra_score + 2
                    #print("자신의 조미료 +5점", user_ingr[i])
            elif ingr_temp[i][4] == 0:
                print("재료번호 X") 
            else:
                if sub_score <=20:
                    sub_score = sub_score +10
                    #print("자신의 부재료 +10", user_ingr[i])
                elif 20 <=sub_score <25:
                    sub_score = sub_score + 5
                    
        My_matching_score= main_score + sub_score + extra_score

    #my_star = My_matching_score / 10
    else:
        My_matching_score=0

    ##################################취향 랭킹######################
    cur = mydb.cursor()  
    cur.execute("SELECT * FROM user_select where id like '"+user+"' order by YMD desc;")
    usertend = cur.fetchall()
    
    if usertend != []:

        xxdf = pd.DataFrame(usertend)
        tend = pd.DataFrame([[0 for j in range(1,5)] for i in range(1,8)], index = [j for j in range(1,8)], columns = [j for j in range(1,5) ])
        main_cook = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[5][x]), range(len(xxdf))))
        code_sum = list(map(lambda x : str(xxdf[3][x])+ str(xxdf[4][x])+ str(xxdf[5][x]), range(len(xxdf))))
        
        for i in range(len(main_cook)):
            tend[int(main_cook[i][0])][int(main_cook[i][1])] = tend[int(main_cook[i][0])][int(main_cook[i][1])] +1 
         
        code_sumdict = sorted(get_count(code_sum).items(), key = lambda item: item[1], reverse = True)
    
    
        sel_main = {}
        sel_cook = {}
        for i in range(1,5):
            #print(i," : ",tend[i].sum())
            sel_main[i] = tend[i].sum()                                  
        topmain1 = max(sel_main,key=sel_main.get)
        del sel_main[ max(sel_main,key=sel_main.get) ]
        topmain2 = max(sel_main,key=sel_main.get)
        # del sel_main[ max(sel_main,key=sel_main.get) ]
        # topmain3 = max(sel_main,key=sel_main.get)
        
        for i in range(7):
            #print(i+1," : ",tend.iloc[i].sum())
            sel_cook[i+1] = tend.iloc[i].sum()   
    
        topcook1 =  max(sel_cook,key=sel_cook.get)
        del sel_cook[ max(sel_cook,key=sel_cook.get) ]
        topcook2 =  max(sel_cook,key=sel_cook.get)
        del sel_cook[ max(sel_cook,key=sel_cook.get) ]
        topcook3 =  max(sel_cook,key=sel_cook.get)   
    
        topcode1 = code_sumdict[0][0]
        topcode2 = code_sumdict[1][0]
        topcode3 = code_sumdict[2][0]
        
        mainrank123 = str(topmain1) + str(topmain2)#+str(topmain3)
        cookrank123 = str(topcook1) + str(topcook2)+str(topcook3)  
        selectrank123 = str(topcode1) +"/"+ str(topcode2)+"/"+str(topcode3)  
        
    else:
        mainrank123 = '0'
        cookrank123 = "0"       
        selectrank123 = "0"
        
    cur.close()
    retval = []
    retval.append(user)
    retval.append(My_matching_score)
    retval.append(mainrank123)
    retval.append(cookrank123)
    retval.append(selectrank123)
    cur.close()
    return retval
#user_score("kmr_friend2")


def exscoredf():
    cur = mydb.cursor()  
    cur.execute("SELECT distinct id FROM user_ingredients;")
    listinuser = cur.fetchall()
    #len( listinuser ) 
    listinuser = list(map(lambda x: listinuser[x][0], range(len(listinuser))))

    userscore = []
    for i in range(len(listinuser)):
        userscore.append(  user_score(listinuser[i]) )
        
    #scoredf = pd.DataFrame(userscore)
    cur.close()
    return userscore
#friend_rank5user("kmr_user")
def friend_rank5user(userid):
    
    #userid = "kmr_user"
    scoredata = exscoredf()
    scoredf = pd.DataFrame(scoredata)
    mydata = scoredf[scoredf[0] == userid]
    mymain = str( int(mydata[2]) )
    mycook = str( int(mydata[3]) )
    myselect = list(mydata[4])[0].split("/")
    
    cur = mydb.cursor() 
    friend_list = []
    try:
         
        cur.execute(f"select friend from user_friends where id = '{userid}' AND accept = 1;")
        friends = cur.fetchall()
        
        friend_list = list(map(lambda x: friends[x][0], range(len(friends))))
        print('친구 조회 성공')
    except:  
        friend_list = []
        print('친구 조회 실패')
        
    #####    
    friends_str_list=[]
    if friend_list:
        
        for f in friend_list:
            try:
                cur.execute(f"select ingredients from user_ingredients where id ='{f}';")
                fri_ing = cur.fetchall()
                friend_str = ', '.join(list(map(lambda x: fri_ing[x][0], range(len(fri_ing)))))
                friends_str_list.append(friend_str)
                print(f'친구 {f} 재료 조회 성공')
            except:
                friends_str_list.append([''])
                print('친구 재료정보 조회 실패')
    ####

    #본인제외 
    scoredf = scoredf[scoredf[0] != userid ]
    scoredf = scoredf.reset_index(drop = True)
    
    frdata = []
    scorefr_df = scoredf
    
    try:
        for i in range(len( friend_list ) ):
            frdata.append( list (  ( scoredf[scoredf[0] == friend_list[i]] ).iloc[0]  ) ) 
            scorefr_df = scorefr_df[scorefr_df[0] != friend_list[i] ]
    except:
        print("friend error")
        
        
    try:
    
        friend_score = []
        for i in range(len(frdata)):
            tendscore,mainscore,cookscore,frscore= 0,0,0,0
            if frdata[i][2] != '0' and scoredf[i][3] !='0' and scoredf[i][4] !='0':
                if frdata[i][2][0] == mymain[0]:
                    mainscore = 10
                elif frdata[i][2][1] == mymain[0]:
                    mainscore = 7
                else:
                    mainscore = 3
                    
                if frdata[i][2][0] == mycook[0]:
                    cookscore = 10
                elif frdata[i][2][1] == mycook[0]:
                    cookscore = 8
                elif frdata[i][2][1] == mycook[0]:
                    cookscore = 5
                else:
                    cookscore = 3
                
                for j in range(3):
                    if frdata[i][4].split("/")[j] in myselect:
                        if frdata[i][4].split("/")[j] == myselect[0]:
                            tendscore = tendscore +10
                        else:
                            tendscore = tendscore + 7
           
            frscore = frdata[i][1]+ mainscore + cookscore + tendscore
            friend_score.append(frscore)
    
    except:
        print("cherck error")
    
    
    
    
    scoredf = scorefr_df.reset_index(drop = True)

    friendscore = []
    for i in range(len(scoredf)):
        tendscore,mainscore,cookscore,frscore= 0,0,0,0
        if int( scoredf[2][i] ) != '0' and scoredf[3][i] !='0' and scoredf[4][i] !='0':
            if scoredf[2][i][0] == mymain[0]:
                mainscore = 10
            elif scoredf[2][i][1] == mymain[0]:
                mainscore = 7
            else:
                mainscore = 3
                
            if scoredf[3][i][0] == mycook[0]:
                cookscore = 10
            elif scoredf[3][i][1] == mycook[0]:
                cookscore = 8
            elif scoredf[3][i][1] == mycook[0]:
                cookscore = 5
            else:
                cookscore = 3
            
            for j in range(3):
                if scoredf[4][i].split("/")[j] in myselect:
                    if scoredf[4][i].split("/")[j] == myselect[0]:
                        tendscore = tendscore +10
                    else:
                        tendscore = tendscore + 7
        
        frscore = scoredf[1][i]+ mainscore + cookscore + tendscore
        friendscore.append(frscore)
        
    scoredf[5] = friendscore
    top5 = scoredf.sort_values(by =5, ascending = False )[:][:5]
    top5id = list(top5[0])
    top5score = list(top5[5])

    top5user_str_list = []

    for i in range(len(top5id)):
        try:
            cur.execute(f"select ingredients from user_ingredients where id ='{top5id[i]}';")
            top5user = cur.fetchall()
            top5user_str = ', '.join(list(map(lambda x: top5user[x][0], range(len(top5user)))))
            top5user_str_list.append(top5user_str)
            print(f'친구 {top5id[i]} 재료 조회 성공')
        except:
            top5user_str_list.append([])
            print('친구 재료정보 조회 실패')   


    cur.close()
    
    return friend_list, friends_str_list, friend_score, top5id ,top5user_str_list,top5score

