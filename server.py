from flask import Flask, render_template


app = Flask(__name__)
port = 8090
host = "127.0.0.1"


@app.route("/<title>")
def main(title):
    return render_template("main.html", title=title)


@app.route("/training/<prof>")
def training(prof):
    return render_template("training.html", prof=prof, title=prof)


if __name__ == '__main__':
    app.run(port=port, host=host)
