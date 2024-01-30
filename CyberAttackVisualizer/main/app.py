import json
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
import pandas as pd
import plotly.express as px
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Function to fetch live cyber attack data (you can replace this with your own data source)
def fetch_cyber_attack_data():
    # Replace the URL with your own data source
    url = "https://api.example.com/cyber-attacks"
    response = requests.get(url)
    data = response.json()
    return data

# Function to update the live data and emit it to the connected clients
def update_live_data():
    cyber_attack_data = fetch_cyber_attack_data()

    # Process the data as needed (example: creating a DataFrame)
    df = pd.DataFrame(cyber_attack_data)

    # Create a Plotly figure
    fig = px.scatter_geo(
        df,
        locations="country",
        locationmode="country names",
        color="attacks",
        size="attacks",
        hover_name="country",
        title="Live Cyber Attacks Across the World",
        template="plotly_dark",
        color_continuous_scale="reds",
        projection="natural earth",
    )

    # Convert the figure to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Emit the updated data to all connected clients
    socketio.emit("update_graph", {"data": graph_json})

# Define the main route
@app.route("/")
def index():
    return render_template("index.html")

# Define the socket connection event
@socketio.on("connect")
def handle_connect():
    print("Client connected")

# Define the periodic data update event
@socketio.on("update_request")
def handle_update_request():
    update_live_data()

if __name__ == "__main__":
    # Start the Flask app with Socket.IO support
    socketio.run(app, debug=True)