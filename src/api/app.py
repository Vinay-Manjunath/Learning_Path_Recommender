from flask import Flask, request, jsonify
from flask_cors import CORS
from src.models.recommend import generate_learning_path

app = Flask(__name__)
CORS(app)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    interests = data.get("interests", [])

    results = generate_learning_path(interests)

    return jsonify(results.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)