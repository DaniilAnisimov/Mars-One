from flask import Flask, render_template


app = Flask(__name__)
port = 8090
host = "127.0.0.1"


@app.route("/")
def main():
    return render_template("main.html", title="123")


if __name__ == '__main__':
    app.run(port=port, host=host)
