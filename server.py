from flask import Flask, render_template


app = Flask(__name__)
port = 8080
host = "127.0.0.1"


@app.route("/")
@app.route("/<title>")
def main(title=""):
    return render_template("base.html", title=title)


@app.route("/training/<prof>")
def training(prof):
    return render_template("training.html", prof=prof, title=prof)


@app.route("/list_prof/<list>")
def list_prof(list):
    return render_template("list_prof.html", list=list)


if __name__ == '__main__':
    app.run(port=port, host=host)
