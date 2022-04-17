from datetime import datetime
from api import api, sql_provider
from api.models.shemas import Student

def do_on_complete(student_id, test_name, job_name):
    patch = {'rk1_finish_time': datetime.now().isoformat()} \
             if test_name == 'rk1' \
             else {'rk2_finish_time': datetime.now().isoformat()}
    sql_provider.update(Student, student_id, patch)
    print(f'Планировщик с именем {job_name} завершил работу')
    api.apscheduler.remove_job(job_name)