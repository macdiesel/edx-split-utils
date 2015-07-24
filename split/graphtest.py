from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/test')
def graph_test():
    return render_template('graphtest.html')


if __name__ == '__main__':
    app.run()
