
import json
import re,random,os
from functools import wraps

from flask import Flask,render_template,request,redirect,flash,session,make_response

from sqlalchemy.sql import text

from wapp import app,csrf
from wapp.models import db,User,Contact,Category,SubCategory,Portfolio
from wapp.forms import ContactUs

#login_required start
def login_required(f):
    @wraps(f) #from functools import wraps
    def login_decorator(*args,**kwargs):
        if session.get("userid") and session.get('user_loggedin'):
           return f(*args,**kwargs)
        else:
            return redirect("/sign/")
    return login_decorator
#login_required end


# sign start
@app.route('/sign/', methods=['POST','GET'])
def sign():
    if request.method =='GET':
        return render_template('Sign.html.', pagename ='Sign Up on Workdun-Hire Freelancers & Get Freelance Jobs Online Workdun.com')
    else:
        fname = request.form.get('fname')
        password = request.form.get('password')
        country = request.form.get('country')
        email = request.form.get('mail')
        
        pattern = ('^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z][A-Za-z0-9!@#$%^&*(),.?":{}|<>]{7}$')
        check = re.match(pattern, password)
        if not check:
            return redirect('/sign/')
        if check:
            users = User(user_fname=fname,user_email=email,user_password=password,user_country=country)
            db.session.add(users)
            db.session.commit()
            #log the user in and redirect to dashboard using u.user_id
            session['userid'] = users.user_id
            session['user_loggedin']=True
            return redirect('/userspro/')
# sign end       
        
         
# userspro start  
@app.route('/userspro/', methods=['POST','GET'])
def userprofile():
    if request.method=='GET':
        return render_template('user/usersprofile.html')
    else:
        usertype = request.form.get('rad')
        if usertype != None:
            return redirect('/profile/')
        else:
             return render_template('user/usersprofile.html')
# userspro end         


# profile start 
@app.route('/profile/',methods=['POST',"GET"])
@login_required
def createprofile():
    useronline = session.get('userid') 
    userdeets = db.session.query(User).get(useronline) 
    if request.method == "GET":  
        return render_template('user/profile.html',userdeets=userdeets)
    else:
        fullname = request.form.get('fullname')
        pix = request.files.get('pix')
        desc = request.form.get('message')
        lang = request.form.get('lang')
        langl = request.form.get('Language')
        skill = request.form.get('skill')
        skillev = request.form.get('skills')
        if pix !='':
            filename = pix.filename
            allowed =['.jpg','.png','.jpeg']
            name,ext = os.path.splitext(filename)
            newname = str(random.random()*1000000) + ext
            if ext.lower() in allowed:
                pix.save('wapp/static/image/profiles/'+ newname)
                userdeets.user_fname=fullname 
                userdeets.user_pix=newname
                userdeets.user_desc =desc
                userdeets.user_lang =lang
                userdeets.user_lang_level=langl
                userdeets.user_skill =skill
                userdeets.user_skill_level =skillev
                db.session.commit()
                return redirect("/dashboard/") 
            else:
                return render_template('user/profile.html',userdeets=userdeets)
# profile end        
            
        
# profilesetting start           
@app.route('/profilesetting/',methods=['POST',"GET"])
@login_required
def profile_setting():
    useronline = session.get('userid') 
    userdeets = db.session.query(User).get(useronline) 
    if request.method == "GET":  
        return render_template('user/settings.html',userdeets=userdeets)
    else:
        fullname = request.form.get('fullname')
        pix = request.files.get('pix')
        if pix !='':
            filename = pix.filename
            allowed =['.jpg','.png','.jpeg']
            name,ext = os.path.splitext(filename)
            newname = str(random.random()*1000000) + ext
            if ext.lower() in allowed:
                pix.save('wapp/static/image/profiles/'+ newname)
                userdeets.user_fname=fullname 
                userdeets.user_pix=newname
                db.session.commit()
                return redirect("/dashboard/") 
            else:
                return render_template('user/settings.html',userdeets=userdeets)
# profilesetting end          
            
            
# dashboard start 
@app.route('/dashboard/')
@login_required
def user_dashboard():
    useronline = session.get('userid')    
    userdeets = db.session.query(User).get(useronline)
    books = SubCategory.query.all()
    cats = db.session.query(Category).all()
    return render_template('user/dashboard.html',userdeets=userdeets,books=books,cats=cats)
# dashboard send              
         

# /user/profile/ start                
@app.route('/user/profile/',methods=['POST',"GET"])
def user_profile():
    useronline = session.get('userid') 
    userdeets = db.session.query(User).get(useronline) 
    return render_template('user/updateprofile.html',userdeets=userdeets)
# /user/profile/ end   



#together
@app.route('/about/')
def about():
    form =ContactUs()
    return render_template('About.html', pagename ='About Workdun-Hire Professional Freelance and Find Freelance work',form=form)

    
@app.route('/submit/contact',methods=['POST'])
def submit_contact_ajax():
    form = ContactUs()
    if form.validate_on_submit():
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')
        c = Contact(cont_name=name,cont_phone=phone,cont_email=email,cont_msg=message) 
        db.session.add(c)
        db.session.commit()
        if c.id:
            sendback={"msg":f"Thank you {name} for contacting us","msgclass":'alert alert-success'}
        else:
            sendback={"msg":"please try again","msgclass":'alert alert-danger'}  
    else:
        sendback={"msg":"form validation failed","msgclass":'alert alert-danger'}
    return json.dumps(sendback)
# end together  


# signout start
@app.route("/signout")  
def signout():
    if session.get('userid') or session.get('user_loggedin'):
        session.pop('userid',None)
        session.pop('user_loggedin',None)
    return redirect("/")
#signout end


# login start         
@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('Login.html', pagename='Log In to Workdun-Freelance MarketPlace Platform Workdun.com')
    else:
        users = request.form.get('user')
        password = request.form.get('pass') 
        deets = db.session.query(User).filter(User.user_fname==users, User.user_password==password).first()
        if deets:
            session['user_loggedin'] = True
            session['userid'] = deets.user_id
            return redirect("/dashboard/")
        
        if deets != password:
            flash("Invalid password")
            return redirect("/login/") 
        elif deets  != users:
            flash("Invalid username")
            return redirect("/login/") 
        else:
            flash("Invalid credentials")
            return redirect("/login/") 
# login end      
    
       
# postwork start  
@app.route('/postwork/',methods=['POST','GET'])
def post_work(): 
     useronline = session.get('userid') 
     userdeets = db.session.query(User).get(useronline) 
      
     if request.method =='GET':
        cats =db.session.query(Category).all()
        return render_template('user/addcat.html',cats=cats,userdeets=userdeets)
     if request.method =='POST':
         subcaty = request.form.getlist('subcat')
         subcat = ','.join(map(str,subcaty))
         bookcat = request.form.get('bookcat')
         title = request.form.get('title')
         cover = request.files.get('cover')
         
         userid = request.form.get('userid')
         subcat = subcat
         if title != '':
            filename = cover.filename
            allowed =['.jpg','.png','.jpeg']
            name,ext = os.path.splitext(filename)
            newname = str(random.random()*1000000) + ext
            if ext.lower() in allowed:
                cover.save('wapp/static/image/collections/'+ newname)
                b = SubCategory(subcat_name=subcat, user_id=userid,subcat_catid=bookcat, subcat_titile=title, subcat_cover=newname)
                db.session.add(b)
                db.session.commit()
                flash('Work  has been added',category='success')
                return redirect('/postwork/')
            else:
                flash('Please upload only type jpeg,png or jpg',category='danger')
                return redirect('/postwork/')
         else:
            flash('Please ensure you complete the required fields',category='danger')
            return redirect('/postwork/')    
# postwork end 


# viewdetails start 
@app.route("/viewdetails/<subcatid>")
def view_detail(subcatid):
    viewdeets = db.session.query(SubCategory).get_or_404(subcatid) 
    userdeets = db.session.query(User).all()
    #userport = db.session.query(Portfolio).all()
    userport = db.session.query(Portfolio).filter_by(port_userid=Portfolio.port_userid).all() 
    return render_template("user/reviews.html",viewdeets=viewdeets,userdeets=userdeets,userport=userport)
# viewdetails end


# portifolio start           
@app.route('/portifolio/',methods=['POST','GET'])
def user_portifolio():
    useronline = session.get('userid') 
    userdeets = db.session.query(User).g#et(useronline)
    if request.method=='GET': 
        return render_template('user/portifolio.html',userdeets=userdeets)
    else:
        desc = request.form.get('description')
        userid = request.form.get('userid')
        pix1 = request.files.get('pix1')
        if pix1 !='':
            filename = pix1.filename
            allowed =['.jpg','.png','.jpeg']
            name,ext = os.path.splitext(filename)
            newname = str(random.random()*1000000) + ext
            if ext.lower() in allowed:
                pix1.save('wapp/static/image/portifolio/'+ newname)
                p = Portfolio(description=desc, sample1=newname,port_userid=userid)
                db.session.add(p)
                db.session.commit()
                flash('portifolio added',category='success')
                return redirect('/portifolio/')
            else:
                flash('Please upload only type jpeg,png,jpg',category='danger')
                return redirect('/portifolio/')
        else:
            flash('Please ensure you complete the required fields',category='danger')
            return redirect('/portifolio/')    
# portifolio end
   
                    
#together
@app.route('/freelancer/')
def freelancer():
    books = SubCategory.query.all()
    cats = db.session.query(Category).all()
    return render_template('Freelancers.html', pagename ='Find Freelancers',books=books,cats=cats)


@app.route('/search/book')
def search_book():
    cate = request.args.get('category')
    title = request.args.get('title') 
    search_title = "%"+title+"%" # "%{}%".format(title)
    #run query
    if cate =="":
        result = db.session.query(SubCategory).filter(SubCategory.subcat_titile.like(search_title)).all()
    else:
        result = db.session.query(SubCategory).filter(SubCategory. subcat_catid==cate).filter(SubCategory.subcat_titile.like(search_title)).all()

    #result = [<Book 1>, <Book 2>, <Book 3>] 
    toreturn = ""
    for r in result:
        toreturn = toreturn + f"<div class='col'><img src='/static/collections/{r.subcat_cover}' class='img-fluid bk'><div class='deets'><h6><a href='/review/{r. subcat_id}'>{r.subcat_titile}</a></h6><p><i>{r.subcategories.cat_name}</i></p><p><button class='btn btn-sm btn-warning'{len(r.bookreviews)}>Reviews</button></p></div></div>"
    
    return toreturn
#end


# home start
@app.route('/')
@app.route('/home/')
def home():
    return render_template('index.html', pagename ='Workdun.com Find and Hire Expert Freelancers')
# home end


# job start  
@app.route('/job/')
def job():
    return render_template('jobs.html', pagename ='Find Freelancer Project and Jobs on Workdun.com')
# job end


# terms_of_service start
@app.route('/workdun/terms_of_service')
def terms_of_service():
    return render_template('Term&service.html')  
# terms_of_service end


# Privacy Policy start
@app.route('/workdun/Privacy-Policy')
def Privacy_Policy():
    return render_template('Privacy&Policy.html')  
# Privacy Policy end
   
