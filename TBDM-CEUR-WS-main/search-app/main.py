from flask import Flask, request, jsonify, render_template
import os
from llm_vector_search import LLMVectorSearch
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
pdf_search = LLMVectorSearch()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if query:
        query_result = pdf_search.search(query)

        result = f"Result for query '{query}': {query_result}"
        return jsonify(result=result)
    else:
        return jsonify(result="No query provided.")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))