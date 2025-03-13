from flask import Flask, render_template, g, redirect, request
from markupsafe import escape


app = Flask(__name__)

def in_paragraphs(text):
    return text.split("\n\n")

def highlight(text, term):
    return text.replace(term, f'<strong>{term}</strong>')

app.jinja_env.filters['highlight'] = highlight

def chapters_matching(query):
    if not query:
        return []

    results = []
    for index, name in enumerate(g.contents, start=1):
        with open(f"book_viewer/data/chp{index}.txt", "r") as file:
            chapter_content = file.read()
        matches = {}
        for para_index, paragraph in enumerate(chapter_content.split("\n\n")):
            if query.lower() in paragraph.lower():
                matches[para_index] = paragraph
        if matches:
            results.append({'number': index, 'name': name, 'paragraphs': matches})

    return results

# Register the filter with the app
app.jinja_env.filters['in_paragraphs'] = in_paragraphs

@app.before_request
def load_contents():
    with open("book_viewer/data/toc.txt", "r") as file:
        g.contents = file.readlines()

@app.errorhandler(404)
def page_not_found(error):
    return redirect("/")

@app.route("/")
def index():
    return render_template('home.html', contents = g.contents)

@app.route("/chapters/<int:chapter_number>")
def chapter(chapter_number):
    chapter_name = g.contents[chapter_number - 1]
    chapter_title = f"Chapter {chapter_number}: {chapter_name}"
    with open(f"book_viewer/data/chp{escape(chapter_number)}.txt", "r") as file:
        text = file.read()

    return render_template('chapter.html',
                            content = text,
                            contents = g.contents,
                            chapter_title = chapter_title)

@app.route("/search")
def search():
    query = request.args.get('query', '')
    
    results = chapters_matching(query) if query else []
    return render_template('search.html', query=query, results=results)

@app.route("/show/")
def show(name):
    return f'{escape(name)}' 


if __name__ == "__main__":
    app.run(debug=True, port=5003)