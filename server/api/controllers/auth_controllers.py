from api import sql_provider
from api.handlers.auth_handler import *
from quart import Blueprint, request, session, make_response

auth = Blueprint('auth', __name__)

@auth.before_app_serving
async def db_init(): 
    await db_init_handler(sql_provider)

@auth.route('/admin_auth', methods=['POST'])
async def admin_auth():
    credentials = await request.get_json()
    token = await admin_auth_handler(sql_provider, credentials)
    return await make_response(*token)

@auth.route('/for_user_auth', methods=['GET'])
async def for_auth():
    for_auth_payload = await for_auth_handler(sql_provider)
    session['group_load'] = for_auth_payload[2]
    for_auth_payload = for_auth_payload[0], for_auth_payload[1]
    return await make_response(*for_auth_payload)

@auth.route('/user_auth', methods=['POST'])
async def user_auth():
    if not session['group_load']:
        return await make_response('Аутентификация невозможна!', 500)
    student_info = await request.get_json()
    student = await user_auth_handler(sql_provider, student_info)
    return await make_response(*student)