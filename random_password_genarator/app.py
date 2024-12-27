from flask import Flask,request,render_template
from datetime import datetime
import random
import string
app=Flask(__name__)
def get_current_datetime():
    current_date=datetime.now().strftime("%d-%B-%Y")
    current_time=datetime.now().strftime("%H:%M:%S")
    return current_date,current_time
@app.route('/')
def home():
    datetoday,timenow = get_current_datetime()
    return render_template('home.html',datetoday=datetoday,timenow=timenow)
@app.route('/genpassword',methods=["POST"])
def gen_password():
    datetoday,timenow=get_current_datetime()
    min_password=8
    max_password=36
    password_len=int(request.form.get('password'))
    if password_len<min_password:
        message = f"Password must be at least {min_password} characters long."
        return render_template('home.html', datetoday=datetoday, timenow=timenow, message=message)
    if password_len>max_password:
        message =f"Password must not exceed {max_password} characters."
        return render_template('home.html', datetoday=datetoday, timenow=timenow, message=message)
    include_spaces=request.form.get('include_spaces')
    include_numbers=request.form.get('include_numbers')
    include_uppercase=request.form.get('include_uppercase')
    include_special_char=request.form.get('include_special')
    lowercase=string.ascii_lowercase
    uppercase=string.ascii_uppercase if include_uppercase=='on' else ''
    digits=string.digits if include_numbers == 'on' else ''
    special_char = string.punctuation if include_special_char=='on' else ''
    spaces =' ' if include_spaces=='on' else ''
    char_all=lowercase+uppercase+digits+special_char+spaces
    if not char_all:
        message="Please select at least one character set for password generation."
        return render_template('home.html',datetoday=datetoday,timenow=timenow,message=message)
    password= ''.join(random.choices(char_all, k=password_len))
    return render_template('home.html',datetoday=datetoday,timenow=timenow,genpassword=password)
if __name__ == '__main__':
    app.run(debug=True)
