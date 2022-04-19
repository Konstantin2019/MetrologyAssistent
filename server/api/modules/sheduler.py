from datetime import datetime
from api import sql_provider
from api.models.shemas import Student

def do_on_complete(student_id, test_name):
    patch = {'rk1_finish_time': datetime.now().isoformat()} \
             if test_name == 'rk1' \
             else {'rk2_finish_time': datetime.now().isoformat()}
    sql_provider.update(Student, student_id, patch)