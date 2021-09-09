from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/scheduler")
def scheduler():
    return render_template("dynamicTable.html")
    
if __name__ == "__main__":
    app.run(debug=True,port="8080")