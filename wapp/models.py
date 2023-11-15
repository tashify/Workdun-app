from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    admin_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    admin_name = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    
    
class SubCategory(db.Model):
    __tablename__='subcategory'
    subcat_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    subcat_name = db.Column(db.String(255), nullable=False)
    subcat_catid = db.Column(db.Integer, db.ForeignKey('category.cat_id'),nullable=False)
    subcat_titile = db.Column(db.Text(),nullable=False)
    subcat_cover = db.Column(db.String(100))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    
     #set relationship
    subcategories= db.relationship('Category',backref='mysubcategory') 
    usercat = db.relationship('User', backref='myuser')
    
class Project(db.Model):
    Project_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    project_name = db.Column(db.String(255), nullable=False)
    details = db.Column(db.String(255), nullable=False)
    budject = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    start_date=db.Column(db.DateTime(), default=datetime.utcnow)
    
    project_catid=  db.Column(db.Integer, db.ForeignKey('category.cat_id'),nullable=False)  
    project_subcatid=  db.Column(db.Integer, db.ForeignKey('subcategory.subcat_id'),nullable=False)  
    #set relationship
    projects = db.relationship('SubCategory',backref='myproject')
    projects = db.relationship('Category',backref='myproject')
    

    
class Portfolio(db.Model):
    Portfolio_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    description = db.Column(db.String(255), nullable=False)
    sample1 = db.Column(db.String(255), nullable=False)
    port_userid =  db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    port_date= db.Column(db.DateTime(), default=datetime.utcnow)
     
    #set relationship
    portfolios = db.relationship('User',backref='myportfolio')
    
    
    
    
class Payment(db.Model):
    Pay_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    amount = db.Column(db.Float(), nullable=False)
    payment_date= db.Column(db.DateTime(), default=datetime.utcnow)
    

    pay_userid=db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)   
    pay_bidid=db.Column(db.Integer, db.ForeignKey('projectbid.projectbid_id'),nullable=False) 
    
     #set relationship  
    payments= db.relationship('User',backref='mypayment') 
    payments= db.relationship('Projectbid', backref='mypayment') 
    
    
class Projectbid(db.Model):
    projectbid_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    amount = db.Column(db.Float(), nullable=False)
    status= db.Column(db.String(255), nullable=False)
    

    probid_projectid=db.Column(db.Integer, db.ForeignKey('project.Project_id'),nullable=False) 
    probid_freelancerid=db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    duration=db.Column(db.Float(), nullable=False)
     #set relationship
    projectbids= db.relationship('User',backref='myprojectbid') 
    projectbids= db.relationship('Project', backref='myprojectbid') 
    
   
      
    
class Rating(db.Model):
    rating_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    rating = db.Column(db.Float(), nullable=False)
    rat_userid=  db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
     
    #set relationship
    rating= db.relationship('User',backref='myrating') 
    rat_date = db.Column(db.DateTime(), default=datetime.utcnow)
    
    
    
class Category(db.Model):
    cat_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    cat_name = db.Column(db.String(255), nullable=False)
    

class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
    user_fname = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(20), nullable=False)
    user_country = db.Column(db.String(50), nullable=False)
    user_desc = db.Column(db.String(120),nullable=True)
    user_lang = db.Column(db.String(120),nullable=True) 
    user_lang_level = db.Column(db.String(120),nullable=True) 
    user_skill = db.Column(db.String(120),nullable=True)
    user_skill_level = db.Column(db.String(120),nullable=True)  
    user_pix = db.Column(db.String(120),nullable=True) 
    user_reg_date = db.Column(db.DateTime(), default=datetime.utcnow)
  
  
class Contact(db.Model):
     id = db.Column(db.Integer(), primary_key=True, autoincrement =True)
     cont_name = db.Column(db.String(255), nullable=False)
     cont_phone = db.Column(db.String(20), nullable=False)
     cont_email = db.Column(db.String(255), nullable=False)
     cont_msg = db.Column(db.Text(),nullable=False)
     cont_reg_date = db.Column(db.DateTime(), default=datetime.utcnow)
  
     
    