from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Fake database (just a list in memory)
posts = [
    {"title": "First Post", "content": "Hello, this is my first blog post!"},
    {"title": "Flask Blog", "content": "Flask makes web apps easy and fun!"},
]

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        posts.append({"title": title, "content": content})
        return redirect(url_for("index"))
    return render_template("new.html")

if __name__ == "__main__":
    app.run(debug=True)
