from flask import Blueprint, request, jsonify
import traceback

from services.ai import get_ai_client
from utils.prompts import system_prompt
from utils.validators import ValidationError, required_fields, validate_messages

bot_bp = Blueprint('bot', __name__)


@bot_bp.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.get_json()
        required_fields(data, ["messages"])
        validate_messages(data["messages"])

        ai = get_ai_client()
        bot_response = ai.chat(data["messages"], system=system_prompt)

        return jsonify({"response": bot_response}), 200

    except ValidationError as e:
        return jsonify({"msg": e.message}), e.status_code
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg": "Failed to process chatbot request", "details": str(e)}), 500
