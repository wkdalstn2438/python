from flask import *
from github import Github, Auth

app = Flask(__name__, static_folder='./static/resource')
g = Github(auth=Auth.Token('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'))

# 테스트 1
@app.route('/hello-world')
def hello_world():
    return 'Hello World!'


# 테스트 2
@app.route('/hello-world2')
def hello_world2():
    return send_file('static/test.html')


# 홈 (index)
@app.route('/')
def index():
    return send_file('static/index.html')


# 연습장 (practice)
@app.route('/practice')
def practice():
    return send_file('static/practice.html')


@app.route('/practice/submit-test', methods=['POST'])
def submit_test():
    my_string = request.form['my-string']
    return f'서버에서 받은 값 {my_string}'


@app.route('/practice/submit-test-async', methods=['POST'])
def submit_test_async():
    my_string = request.form['my-string']
    return f'(비동기) 서버에서 받은 값 {my_string}'


@app.route('/git/user')
def git_user_info():
    user = g.get_user()
    return jsonify({
        'nickname': user.login,
        'name': user.name,
        'email': user.email,
        'img': user.avatar_url,
        'url': user.html_url
    })


@app.route('/git/repo')
def git_repo_list():
    repo = g.get_user().get_repos()
    repo_list = []
    for r in repo:
        repo_list.append({
            'title': r.name,
            'url': r.html_url
        })
    return jsonify(repo_list)


@app.route('/git/gist')
def git_gist_list():
    gist = g.get_user().get_gists()
    gist_list = []
    for _g in gist:
        gist_list.append({
            'filename': list(_g.files.keys())[0],
            'url': _g.html_url
        })
    return jsonify(gist_list)


if __name__ == '__main__':
    app.run()
