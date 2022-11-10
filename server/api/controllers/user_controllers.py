from api import api, sql_provider
from quart import Blueprint, request, make_response, send_from_directory
from api.handlers.user_handler import *

user = Blueprint('user', __name__)

@user.route('/download/<path:filename>', methods=['GET'])
async def download(filename):
    response = await send_from_directory(api.config['UPLOAD_FOLDER'], filename)
    return response

@user.route('/test/<int:student_id>/<string:rk_choice>/<string:teacher>', methods=['GET'])
async def get_test(student_id: int, rk_choice: str, teacher: str):
    user_data = await get_test_handler(sql_provider, student_id, rk_choice, teacher)
    return await make_response(*user_data)

@user.route('/test/<int:student_id>/<string:rk_choice>/<string:teacher>', methods=['POST'])
async def send_test(student_id: int, rk_choice: str, teacher: str):
    user_answer = await request.get_json()
    send_result = await send_test_handler(sql_provider, student_id, rk_choice, teacher, user_answer) 
    return await make_response(*send_result)