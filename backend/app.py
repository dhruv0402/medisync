from flask import Flask
from utils.db import get_db_connection
from utils.db import execute_query

app = Flask(__name__)

@app.route("/")
def home():
    return "MediSync Backend Running Successfully 🚀"
@app.route("/test-db")
def test_db():
    result = execute_query("SELECT NOW()")
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)

