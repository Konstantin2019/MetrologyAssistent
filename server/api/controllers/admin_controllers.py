from api import sql_provider
from quart import Blueprint, request, make_response, Response
from api.handlers.admin_handler import *
from api.models import Admin

admin = Blueprint('admin', __name__)

@admin.before_request
async def admin_middleware():
    token = request.args.get('token')
    if token:
        admin: Admin = await sql_provider.get(Admin, key={'id': 1})
        if admin and admin.token == token:
            return None
    return await make_response('Не авторизован!', 401)

@admin.after_request
async def response_wrapper(response: Response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@admin.route('/', methods=['GET'])
async def admin_index():
    admin_info = await admin_index_handler(sql_provider)
    return await make_response(*admin_info)     
    
@admin.route('/create_group', methods=['POST'])
async def create_group():
    group_data = await request.get_json()
    creation_result = await create_group_handler(sql_provider, group_data)
    return await make_response(*creation_result) 
    
@admin.route('/del_group/<int:group_id>', methods=['DELETE'])
async def del_group(group_id):
    del_result = await del_group_handler(sql_provider, group_id)
    return await make_response(*del_result)

@admin.route('/add_students', methods=['POST'])
async def add_students():
    students_data = await request.get_json()
    add_result = await add_students_handler(sql_provider, students_data)
    return await make_response(*add_result)    
    
@admin.route('/view_student/<int:student_id>', methods=['GET'])
async def view_student(student_id):
    rk = request.args.get('rk')
    questions = await view_student_handler(sql_provider, student_id, rk)
    return await make_response(*questions)

@admin.route('/del_student/<int:student_id>', methods=['DELETE'])
async def del_student(student_id):
    del_result = await del_student_handler(sql_provider, student_id)
    return await make_response(*del_result)

@admin.route('/patch_score/<int:question_id>', methods=['POST'])
async def patch_score(question_id):
    score = await request.get_json()
    patch_result = await patch_score_handler(sql_provider, question_id, score)
    return await make_response(*patch_result)

@admin.route('/patch_answer/<int:question_id>', methods=['POST'])
async def patch_answer(question_id):
    answer = await request.get_json()
    patch_result = await patch_answer_handler(sql_provider, question_id, answer)
    return await make_response(*patch_result)

@admin.route('/patch_email/<int:student_id>', methods=['POST'])
async def patch_email(student_id):
    email = await request.get_json()
    patch_result = await patch_email_handler(sql_provider, student_id, email)
    return await make_response(*patch_result)

@admin.route('/del_questions', methods=['DELETE'])
async def del_questions():
    student_id = request.args.get('student_id')
    test_name = request.args.get('test_name')
    del_result = await del_questions_handler(sql_provider, student_id, test_name)
    return await make_response(*del_result)