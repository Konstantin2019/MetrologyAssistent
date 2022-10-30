import * as XLSX from 'xlsx';
import * as FileSaver from 'file-saver';
import axios from 'axios';

const AddGroup = (groupName, setGroupName, setReload, navigate) => {
    let url = '/api/admin/create_group';
    let token = sessionStorage.getItem('token');
    axios.post(url, { group_name: groupName }, { params: { token: token } })
        .then(res => res.data)
        .then(groupId => {
            alert(`Группа c id = ${groupId} успешно добавлена или уже существует!`);
            setGroupName('');
            setReload(reload => reload + 1);
        })
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

const DelGroup = (groups, groupName, setGroupName, setReload, navigate) => {
    let group = groups.filter(g => g.group_name === groupName)[0];
    let url = `/api/admin/del_group/${group.id}`;
    let token = sessionStorage.getItem('token');
    axios.delete(url, { params: { token: token } })
        .then(res => res.data)
        .then(groupId => {
            alert(`Группа c id = ${groupId} успешно удалена!`);
            setGroupName('');
            setReload(reload => reload + 1);
        })
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

const AddStudent = (surname, setSurname, name, setName, patronymic, setPatronymic, email, setEmail, selectedGroup, setReload, navigate) => {
    if (patronymic === (undefined || null)) {
        patronymic = ''
    }
    let student = {
        surname: surname.replace(/\s+/g, ''),
        name: name.replace(/\s+/g, ''),
        patronymic: patronymic.replace(/\s+/g, ''),
        email: email.replace(/\s+/g, '').toLowerCase(),
        group_id: selectedGroup.id
    };
    let url = '/api/admin/add_students';
    let token = sessionStorage.getItem('token');
    axios.post(url, { students: student }, { params: { token: token } })
        .then(res => res.data)
        .then(studentId => {
            alert(`Студент c id = ${studentId} успешно добавлен или уже существует!`);
            setSurname('');
            setName('');
            setPatronymic('');
            setEmail('');
            setReload(reload => reload + 1);
        })
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

const ReadExcel = (e) => {
    let excelFile = e.target.files[0];
    let promise = new Promise((resolve, reject) => {
        let fileReader = new FileReader();
        fileReader.readAsArrayBuffer(excelFile);
        fileReader.onload = (e) => {
            let buffer = e.target.result;
            let workbook = XLSX.read(buffer, { type: 'buffer' });
            let sheetName = workbook.SheetNames[0];
            let sheet = workbook.Sheets[sheetName];
            let data = XLSX.utils.sheet_to_json(sheet);
            resolve(data);
        };
        fileReader.onerror = (e) => reject(e);
    });
    e.target.value = null;
    return promise;
};

const LoadToExcel = (students, fileName) => {
    let studentsToLoad = students.map(student => {
        let studentToLoad = {
            Фамилия: student.surname,
            Имя: student.name,
            Отчество: student.patronymic,
            РК1: student.rk1_score,
            РК2: student.rk2_score,
            Зачёт: student.test_score
        };
        return studentToLoad;
    });
    let fileType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
    let fileExtension = '.xlsx';
    let worksheet = XLSX.utils.json_to_sheet(studentsToLoad);
    let workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, fileName);
    let excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    let result = new Blob([excelBuffer], { type: fileType });
    FileSaver.saveAs(result, fileName + fileExtension);
};

const AddStudents = (studentsPromise, groups, setReload, navigate) => {
    studentsPromise.then(records => {
        let students = records.map(record => {
            let group_id = groups.filter(g => g.group_name === record.Группа).map(g => g.id)[0];
            if (!record.hasOwnProperty('Отчество')) {
                record.Отчество = ''
            };
            let student = {
                surname: record.Фамилия.replace(/\s+/g, ''),
                name: record.Имя.replace(/\s+/g, ''),
                patronymic: record.Отчество.replace(/\s+/g, ''),
                email: record.Почта.replace(/\s+/g, '').toLowerCase(),
                group_id: group_id
            };
            return student;
        }).filter(s => s.group_id !== (null || undefined));
        return students;
    }).then(loadedStudents => {
        let url = '/api/admin/add_students';
        let token = sessionStorage.getItem('token');
        axios.post(url, { students: loadedStudents }, { params: { token: token } })
            .then(res => res.data)
            .then(studentsIds => {
                alert(`Студенты c ids = [${studentsIds}] успешно добавлены или уже существуют!`);
                setReload(reload => reload + 1);
            })
            .catch(err => {
                if (err.response.status === 401) { navigate('/admin_auth') }
                else { alert(err.response.data) }
            });
    }).catch(err => alert(err.message));
};

const DelStudent = (studentId, setReload, navigate) => {
    let url = `/api/admin/del_student/${studentId}`;
    let token = sessionStorage.getItem('token');
    axios.delete(url, { params: { token: token } })
        .then(res => res.data)
        .then(studentId => {
            alert(`Студент c id = ${studentId} успешно удален!`);
            setReload(reload => reload + 1);
        })
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

const DelQuestions = (studentId, testName, setReload, navigate) => {
    let url = '/api/admin/del_questions';
    let token = sessionStorage.getItem('token');
    axios.delete(url, { params: { student_id: studentId, test_name: testName, token: token } })
        .then(_ => {
            alert(`Вопросы успешно сброшены!`);
            setReload(reload => reload + 1);
        })
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

const patchAnswer = (questionId, answer, testName, setReload, navigate) => {
    let url = `/api/admin/patch_answer/${questionId}`;
    let token = sessionStorage.getItem('token');
    axios.post(url, { rk: testName, answer: answer }, { params: { token: token } })
        .then(_ => setReload(reload => reload + 1))
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

const patchScore = (questionId, score, testName, setReload, navigate) => {
    let url = `/api/admin/patch_score/${questionId}`;
    let token = sessionStorage.getItem('token');
    axios.post(url, { rk: testName, question_score: score }, { params: { token: token } })
        .then(_ => setReload(reload => reload + 1))
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

const patchEmail = (studentId, email, setReload, navigate) => {
    let url = `/api/admin/patch_email/${studentId}`;
    let token = sessionStorage.getItem('token');
    axios.post(url, { email: email }, { params: { token: token } })
        .then(_ => setReload(reload => reload + 1))
        .catch(err => {
            if (err.response.status === 401) { navigate('/admin_auth') }
            else { alert(err.response.data) }
        });
};

export { AddGroup, AddStudent, AddStudents, DelGroup, DelStudent, ReadExcel, LoadToExcel, DelQuestions, patchAnswer, patchScore, patchEmail }