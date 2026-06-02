from flask import Flask, render_template, jsonify, request
from ebird_client import EBirdClient
from data import get_cached_observations, get_yearly_observations, build_presence_matrix, sort_matrix

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/observations")
def observations():
    region = request.args.get("region", "US-NM")
    client = EBirdClient(region)
    yearly = get_cached_observations(client)
    matrix = sort_matrix(build_presence_matrix(yearly)) 
    serializable = {species: bird.to_dict() for species, bird in matrix.items()}
    return jsonify(serializable)
if __name__ == "__main__":
    app.run(debug=True)
