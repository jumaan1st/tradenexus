from flask import Blueprint, request, jsonify
import traceback

from services.ai import get_ai_client
from utils.prompts import system_prompt

bot_bp = Blueprint('bot', __name__)


@bot_bp.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.get_json()
        messages = data.get('messages', [])

        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        ai = get_ai_client()
        bot_response = ai.chat(messages, system=system_prompt)

        return jsonify({"response": bot_response}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Failed to process chatbot request", "details": str(e)}), 500
