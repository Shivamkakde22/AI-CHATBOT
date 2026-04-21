# app.py is your main file that:

# Starts the Flask server
# Handles user requests
# Connects frontend ↔ backend


from flask import Flask,render_template, request,redirect,url_for
from anthropic_serv import generate_response
from db import get_connection

app = Flask(__name__)
secret = "your_secret_key_here"
app.secret_key = secret

@app.route('/')
def home():
    """Render the home page with chat history."""
    conn = get_connection()
    curr = conn.cursor()
    
    curr.execute("Select sender,message from chat_history ORDER BY id ASC")
    rows = curr.fetchall()
    
    chat_history = []
    for row in rows:
        chat_history.append({
            "sender":row[0],
            "text":row[1]
        })
    curr.close()
    conn.close()
    return render_template('index.html', chat_history=chat_history)
    

@app.route('/chat', methods=['POST'])
def handle_chat():
    """Handle chat request and return bot response."""
    user_input = request.form.get("message")
    
    conn = get_connection()
    curr = conn.cursor()
    
    # Store user chat in db
    curr.execute("Insert into chat_history (sender,message) Values (%s,%s)", ("user", user_input))
    
    # get full chat history
    curr.execute("Select sender,message from chat_history ORDER BY id ASC")
    rows = curr.fetchall()
    
    chat_history = [
        {"sender": r[0], "text": r[1]} for r in rows
    ]
    
    # get response from bot
    bot_response = generate_response(chat_history)
    
    # Save bot response in db
    curr.execute("Insert into chat_history (sender,message) Values (%s,%s)", ("bot", bot_response))
    
    conn.commit()
    curr.close()
    conn.close()
    return redirect(url_for('home'))

app.route('/clear',methods=['POST'])
def clear_history():
    """Clear chat history from db."""
    conn = get_connection()
    if conn is None:
        return "Database connection error"
    curr = conn.cursor()
    
    curr.execute("DELETE FROM chat_history")
    
    conn.commit()
    curr.close()
    conn.close()
    return redirect(url_for('home'))


if __name__== '__main__':
    app.run(debug=True)