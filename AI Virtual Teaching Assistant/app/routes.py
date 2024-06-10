from flask import render_template, request, jsonify, redirect, url_for, session,Response, stream_with_context
from app import app, db
from app.models import Chat
import uuid
from app.AIcomponent import get_ai_response  

@app.route('/')
def index():
    session.pop('session_id', None)
    session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.form.get('user_message')

    if user_message is None or user_message.strip() == "":
        return jsonify({'error': 'User message cannot be empty'}), 400

    session_id = session.get('session_id')

    chat_entries = Chat.query.filter_by(session_id=session_id).order_by(Chat.timestamp).all()
    conversation_history = [entry.message for entry in chat_entries]

    conversation_history.append(f"Human: {user_message}")

    ai_response = get_ai_response(conversation_history)
    conversation_history.append(f"Assistant: {ai_response}")

    user_message_entry = Chat(message=f"Human: {user_message}", session_id=session_id)
    db.session.add(user_message_entry)

    ai_response_entry = Chat(message=f"Assistant: {ai_response}", session_id=session_id)
    db.session.add(ai_response_entry)

    db.session.commit()

    return jsonify({'user_message': user_message, 'bot_response': ai_response})

@app.route('/start-new-session', methods=['POST'])
def start_new_session():
    previous_session_id = request.form.get('previous_session_id')

    if previous_session_id:
        previous_chat_entries = Chat.query.filter_by(session_id=previous_session_id).all()
        previous_conversation_history = [entry.message for entry in previous_chat_entries]
    else:
        previous_conversation_history = []

    session.pop('session_id', None)
    session['session_id'] = str(uuid.uuid4())

    if previous_conversation_history:
        chat_entry = Chat(message="\n".join(previous_conversation_history), session_id=session['session_id'])
        db.session.add(chat_entry)
        db.session.commit()

    if previous_session_id:
        Chat.query.filter_by(session_id=previous_session_id).delete()
        db.session.commit()

    return jsonify({'success': True})


@app.route('/get-session-id', methods=['GET'])
def get_session_id():
    session_id = session.get('session_id')
    if session_id:
        return jsonify({'session_id': session_id})
    else:
        return jsonify({'error': 'No session found'}), 404

@app.route('/delete-session', methods=['POST'])
def delete_session():
    session_id_to_delete = request.form.get('session_id')
    if session_id_to_delete:
        Chat.query.filter_by(session_id=session_id_to_delete).delete()
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Invalid session ID'}), 400

@app.route('/chat-history', methods=['GET'])
def chat_history():
    chat_entries = Chat.query.order_by(Chat.session_id, Chat.timestamp).all()
    chat_history = [entry.to_dict() for entry in chat_entries]
    return jsonify({'chat_history': chat_history})

@app.route('/get-conversation-history', methods=['POST'])
def get_conversation_history():
    session_id = request.form.get('session_id')
    if session_id:
        chat_entries = Chat.query.filter_by(session_id=session_id).order_by(Chat.timestamp).all()
        conversation_history = [entry.message for entry in chat_entries]
        return jsonify({'conversation_history': conversation_history})
    else:
        return jsonify({'error': 'Invalid session ID'}), 400
    


# @app.route('/resume-session', methods=['POST'])
# def resume_session():
#     session_id = request.form.get('session_id')
#     if session_id:
#         chat_entries = Chat.query.filter_by(session_id=session_id).order_by(Chat.timestamp).all()
#         conversation_history = [entry.message for entry in chat_entries]
#         session['session_id'] = session_id
#         return jsonify({'conversation_history': conversation_history})
#     else:
#         return jsonify({'error': 'Invalid session ID'}), 400
    
    
# @app.route('/api/chat', methods=['POST'])
# def chat():
#     user_message = request.form.get('user_message')

#     if user_message is None or user_message.strip() == "":
#         return jsonify({'error': 'User message cannot be empty'}), 400

#     session_id = session.get('session_id')

#     # Retrieve the existing conversation history for the current session
#     existing_chat = Chat.query.filter_by(session_id=session_id).first()
#     if existing_chat:
#         conversation_history = existing_chat.conversation_history.split("\n")
#     else:
#         conversation_history = []

#     # Append the new message to the conversation history
#     conversation_history.append(f"Human: {user_message}")

#     # Get the AI response and append it to the conversation history
#     ai_response = get_ai_response(conversation_history)
#     conversation_history.append(f"Assistant: {ai_response}")

#     # If an existing chat entry exists, update it with the new conversation history
#     if existing_chat:
#         existing_chat.conversation_history = "\n".join(conversation_history)
#         db.session.commit()
#     # Otherwise, create a new chat entry with the conversation history
#     else:
#         chat_entry = Chat(conversation_history="\n".join(conversation_history), session_id=session_id)
#         db.session.add(chat_entry)
#         db.session.commit()

#     return jsonify({'user_message': user_message, 'bot_response': ai_response})