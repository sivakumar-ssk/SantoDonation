# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 11:00:16 2020

@author: Sai Nidhi
"""

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def check(email):
    url = "https://6khifq9vqf.execute-api.us-east-1.amazonaws.com/plasmask/getdata?email="+email
    status = requests.request("GET",url)
    print(status.json())
    return status.json()


@app.route('/registration')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    x = [x for x in request.form.values()]
    print(x)
    params = "name="+x[0]+"&email="+x[1]+"&phone="+x[2]+"&city="+x[3]+"&infect="+x[4]+"&blood="+x[5]+"&password="+x[6]
    
    if('errorType' in check(x[1])):
        url = "https://6khifq9vqf.execute-api.us-east-1.amazonaws.com/plasmask/registration?"+params
        response = requests.get(url)
        return render_template('register.html', pred="Registration Successful, please login using your details")
    else:
        return render_template('register.html', pred="You are already a member, please login using your details")

@app.route('/')    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    print(user,passw)
    data = check(user)
    if('errorType' in data):
        return render_template('login.html', pred="The username is not found, recheck the spelling or please register.")
    else:
        if(passw==data['password']):
            return redirect(url_for('stats'))
        else:
            return render_template('login.html', pred="Login unsuccessful. You have entered the wrong password.") 
        
        
@app.route('/stats')
def stats():
    url = "https://6khifq9vqf.execute-api.us-east-1.amazonaws.com/plasmask/getbloodgroupdata"
    response = requests.get(url)
    r = response.json()
    print(r)
    return render_template('stats.html',b=sum(r),b1=str(r[0]),b2=str(r[1]),b3=str(r[2]),b4=str(r[3]),b5=str(r[4]),b6=str(r[5]),b7=str(r[6]),b8=str(r[7]))

@app.route('/requester')
def requester():
    return render_template('request.html')


@app.route('/requested',methods=['POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    #print(bloodgrp)
    url = "https://6khifq9vqf.execute-api.us-east-1.amazonaws.com/plasmask/requestonbloodgroupsk?blood="+bloodgrp
    status = requests.request("GET",url)
    a=status.json()
    print(a)
    phone=[]
    for i in a:
        url="https://www.fast2sms.com/dev/bulkV2?authorization=jp7kMrOIvRJPKFNlCtUqchYGb6BELDTQ81ZXHeVu03fSwmWi5Aw9nQihMolgBxaSXjCsKHb4Y1rVW3I0&sender_id=DLT_SENDER_ID&message=Need plasma of your blood group&variables_values=12345|asdaswdx&route=dlt&numbers="+str(i['phone'])
        result=requests.request("GET",url)        
        print(result)
        phone.append(i['phone'])
 
    print(phone)

    return render_template('request.html',pred="Your request is sent to the concerned people.")    
   
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)