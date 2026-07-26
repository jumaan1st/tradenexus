from flask import Blueprint, request, jsonify
import ollama
import traceback

from utils.prompts import system_prompt

bot_bp = Blueprint('bot', __name__)


@bot_bp.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.get_json()
        messages = data.get('messages', [])

        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        conversation = []
        for msg in messages:
            if 'user' in msg:
                conversation.append({"role": "user", "content": msg['user']})
            if 'bot' in msg:
                conversation.append({"role": "assistant", "content": msg['bot']})

        conversation.insert(0, {"role": "system", "content": system_prompt})

        response = ollama.chat(model='llama3.1', messages=conversation)
        bot_response = response['message']['content']

        return jsonify({"response": bot_response}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Failed to process chatbot request", "details": str(e)}), 500
