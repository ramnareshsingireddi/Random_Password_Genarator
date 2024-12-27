import os
from flask import Flask,request,render_template
from datetime import date,datetime
app = Flask(__name__)
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")
if 'tasks.txt' not in os.listdir('.'):
    with open('tasks.txt','w') as f:
        f.write('')
def get_list():
    with open('tasks.txt','r') as f:
        tasklist = f.readlines()
    return tasklist
def create_new_list():
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.write('')
def update_list(tasklist):
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.writelines(tasklist)
@app.route('/')
def home():
    return render_template('home.html',datetoday2=datetoday2,datetoday=datetoday,tasklist=get_list(),l=len(get_list())) 
@app.route('/clear')
def clear_list():
    create_new_list()
    return render_template('home.html',datetoday2=datetoday2,datetoday=datetoday,tasklist=get_list(),l=len(get_list())) 
@app.route('/addtask',methods=['POST'])
def add_task():
    task = request.form.get('newtask')
    with open('tasks.txt','a') as f:
        f.writelines(task+'\n')
        current_time=datetime.now().strftime("%H:%M:%S")
    return render_template('home.html',datetoday2=datetoday2,datetoday=datetoday,tasklist=get_list(),l=len(get_list())) 
@app.route('/deltask',methods=['GET'])
def remove_task():
    task_index = int(request.args.get('deltaskid'))
    tasklist = get_list()
    print(task_index)
    print(tasklist)
    if task_index < 0 or task_index > len(tasklist):
        return render_template('home.html',datetoday2=datetoday2,current_time=datetime.now().strftime("%H:%M:%S"),datetoday=datetoday,tasklist=tasklist,l=len(tasklist),mess='Invalid Index...') 
    else:
        removed_task = tasklist.pop(task_index)
    update_list(tasklist)
    return render_template('home.html',datetoday2=datetoday2,current_time=datetime.now().strftime("%H:%M:%S"),datetoday=datetoday,tasklist=tasklist,l=len(tasklist)) 
if __name__ == '__main__':
    app.run(debug=True)