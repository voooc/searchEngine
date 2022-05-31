# -!- coding: utf-8 -!-
from 检索.find import Find
from flask import Flask, render_template, request


app = Flask(__name__)


def highlight(docs, terms):
    result = []
    print()
    for doc in docs:
        content = doc[2]
        for term in terms:
            content = content.replace(term, '<em><font color="red">{}</font></em>'.format(term))
        result.append([doc[0], doc[1], content])
    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    input_text = request.form.get('sw')
    a = Find(input_text)
    list_text = a.find()
    list_text = highlight(list_text, input_text)
    return render_template('search.html', docs=list_text, value=input_text, length=len(list_text))


@app.route('/search/<query>', methods=['GET', 'POST'])
def search2(query):
    input_text = request.form.get('query')
    a = Find(input_text)
    list_text = a.find()
    list_text = highlight(list_text, input_text)
    return render_template('search.html', docs=list_text, value=input_text, length=len(list_text))


if __name__ == '__main__':
    app.run()