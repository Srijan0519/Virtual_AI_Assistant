from flask import render_template, request, jsonify, redirect, url_for, session
from app import app, db
from app.models import Chat
import uuid
from app.AIcomponent import get_ai_response  


@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4()) 
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.form.get('user_message')

    if user_message is None or user_message.strip() == "":
        return jsonify({'error': 'User message cannot be empty'}), 400

    session_id = session.get('session_id')

    chat_entry = Chat(user_message=user_message, bot_response="Processing...", session_id=session_id)  # Placeholder response
    db.session.add(chat_entry)
    db.session.commit()

    #ai_response = "dummy response"
    ai_response = get_ai_response(user_message)  # Assuming get_ai_response() function returns the AI's response
    chat_entry.bot_response = ai_response  
    db.session.commit()

    return jsonify({'user_message': user_message, 'bot_response': ai_response})



@app.route('/bot-response')
def bot_response():
    return render_template('bot_response.html')


@app.route('/chat-history')
def chat_history():
    session_id = session.get('session_id')
    chat_entries = Chat.query.filter_by(session_id=session_id).all()
    return render_template('chat_history.html', chat_entries=chat_entries)


@app.route('/delete-chat-entry/<int:entry_id>', methods=['POST'])
def delete_chat_entry(entry_id):
    chat_entry = Chat.query.get_or_404(entry_id)
    db.session.delete(chat_entry)
    db.session.commit()
    return redirect(url_for('chat_history'))
