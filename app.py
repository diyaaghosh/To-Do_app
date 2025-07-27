from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__) # creating an app

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class ToDo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self): # what it shows during print
         return (f"{self.sno} - {self.title}")


@app.route("/", methods=["GET", "POST"])
def html_site():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    search_query = request.args.get("search")
    if search_query:
        alltodo = ToDo.query.filter(ToDo.title.ilike(f"%{search_query}%")).all()
    else:
        alltodo = ToDo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo=ToDo.query.filter_by(sno=sno).first()
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')
    
    
    return render_template("update.html", todo=todo)

if __name__=="__main__": # app run
    app.run(debug=True,port=8000)