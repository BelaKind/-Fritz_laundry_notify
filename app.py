import threading
from flask import Flask, render_template
from main import main_program, get_live_dashboard_data

app = Flask(__name__)

@app.route('/')
def dashboard():
   
    daten = get_live_dashboard_data()
    return render_template('Web Dashboard/index.html')

def run_flask():
    print("starting webserver...")
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    main_program()
    
    