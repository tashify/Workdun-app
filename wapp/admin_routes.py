"""This module will generate a mini webserver"""
from flask import Flask,render_template, request,redirect,flash,make_response,session
from wapp import app
from wapp.models import db,Admin,User,Contact


@app.route("/admin/login",methods=['GET','POST'])
def adminlogin():
    if request.method=='GET':
        return render_template("admin/login.html")
    else:
        username= request.form.get('username')
        pwd= request.form.get('password')
        chk= db.session.query(Admin).filter(Admin.admin_name==username,Admin.admin_password==pwd).count()
        if chk:
            session['admin_loggedin']=True
            return redirect('/admin/dashboard')
        else:
            flash('Incorrect credentials')
            return redirect('/admin/login')
        

@app.route('/admin/logout')
def admin_logout():
    if session.get('admin_loggedin'):
        session.pop('admin_loggedin',None)
        flash('You have logged out successfully...',category="success")
    return redirect('/admin/login')



@app.route("/admin/dashboard")
def adminhome():
     if session.get('admin_loggedin')==None:
        flash("Access Denied",category="danger")
        return redirect('/admin/login')
     return render_template("admin/admin_dashboard.html")



@app.route("/admin/users")
def users():
     userdeets = db.session.query(User).all()
     return render_template("admin/users.html",userdeets=userdeets)
 
 

@app.route("/admin/contact-us")
def contact():
     contactus = db.session.query(Contact).all()
     return render_template("admin/contactus.html",contactus=contactus)
 