from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///test.db"
db = SQLAlchemy(app)

class toDo(db.Model):
    id = db.Column(db.Integer,primary_key = True, nullable=False)
    content = db.Column(db.String(300),nullable=False)
    
    def __rep__(self):
        sentence = "Task " + self.id + " created!"
        return sentence

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == "POST":
        content=request.form["task-content"]
        new_task = toDo(content = content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'
    else:
        tasks = toDo.query.all()
        return render_template("home.html", fuck = tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = toDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an error while deleting the task"

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    task = toDo.query.get_or_404(id)
    if request.method=="POST":
        task.content=request.form["task-content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error while updating the task"
    else:
        return render_template("update.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
