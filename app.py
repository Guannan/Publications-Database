from flask import Flask, request, jsonify, render_template
import sqlite3
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)


def find_relevant_articles(question):
    # Process the question
    processed_question = nlp(question)

    # Connect to the database
    conn = sqlite3.connect('publications.db')
    cursor = conn.cursor()

    # Retrieve all summaries
    cursor.execute("SELECT PublicationID, Title FROM Publications")
    articles = cursor.fetchall()

    # Close the connection
    conn.close()

    # Compare question with each summary
    matches = []
    for article_id, title in articles:
        processed_summary = nlp(title)
        similarity = processed_question.similarity(processed_summary)
        if similarity > 0.15:  # Threshold for similarity
            matches.append(article_id)

    return matches


@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    question = data['question']
    processed_question = nlp(question)

    conn = sqlite3.connect('publications.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Publications")
    articles = cursor.fetchall()

    matches = []
    for article in articles:
        article_id, title, year, journal, summary, methodologies, outcomes, data_sources, research_questions = article
        processed_title = nlp(title)
        similarity = processed_question.similarity(processed_title)
        if similarity > 0.2:
            matches.append({
                "id": article_id,
                "title": title,
                "year": year,
                "journal": journal,
                "summary": summary,
                "methodologies": methodologies,
                "outcomes": outcomes,
                "data_sources": data_sources,
                "research_questions": research_questions
            })

    conn.close()
    return jsonify(matches)


@app.route('/add_publication', methods=['POST'])
def add_publication():
    data = request.json
    title = data['title']
    year = data['year']
    journal = data['journal']
    summary = data['summary']
    methodologies = data['methodologies']
    outcomes = data['outcomes']
    data_sources = data['data_sources']
    research_questions = data['research_questions']

    # Connect to the database
    conn = sqlite3.connect('publications.db')
    cursor = conn.cursor()

    # Insert new publication
    cursor.execute('''
        INSERT INTO Publications (Title, Year, Journal, Summary, Methodologies, Outcomes, DataSources, ResearchQuestions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, year, journal, summary, methodologies, outcomes, data_sources, research_questions))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Publication added successfully"})


@app.route('/update_publication/<int:publication_id>', methods=['PUT'])
def update_publication(publication_id):
    data = request.json
    # Add logic to update the publication with the provided ID
    # using the data received in the request
    # ...

    return jsonify({"success": True, "message": "Publication updated successfully"})


@app.route('/delete_publication/<int:publication_id>', methods=['DELETE'])
def delete_publication(publication_id):
    # Add logic to delete the publication with the provided ID
    # ...

    return jsonify({"success": True, "message": "Publication deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
