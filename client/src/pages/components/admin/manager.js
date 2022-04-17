import * as XLSX from 'xlsx';
import axios from 'axios';

const AddGroup = (groupName, setGroupName, setReload) => {
    let url = '/api/admin/create_group';
    axios.post(url, { group_name: groupName })
        .then(res => res.data)
        .then(groupId => {
            alert(`Группа c id = ${groupId} успешно добавлена или уже существует!`);
            setGroupName('');
            setReload(reload => reload + 1);
        })
        .catch(err => alert(err.response.data));
};

const DelGroup = (groups, groupName, setGroupName, setReload) => {
    let group = groups.filter(g => g.group_name === groupName)[0];
    let url = `/api/admin/del_group/${group.id}`;
    axios.delete(url)
        .then(res => res.data)
        .then(groupId => {
            alert(`Группа c id = ${groupId} успешно удалена!`);
            setGroupName('');
            setReload(reload => reload + 1);
        })
        .catch(err => alert(err.response.data));
};

const AddStudent = (surname, setSurname, name, setName,
    patronymic, setPatronymic, email, setEmail,
    selectedGroup, setReload) => {
    let student = {
        surname: surname,
        name: name,
        patronymic: patronymic,
        email: email,
        group_id: selectedGroup.id
    };
    let url = '/api/admin/add_students';
    axios.post(url, student)
        .then(res => res.data)
        .then(studentId => {
            alert(`Студент c id = ${studentId} успешно добавлен или уже существует!`);
            setSurname('');
            setName('');
            setPatronymic('');
            setEmail('');
            setReload(reload => reload + 1);
        })
        .catch(err => alert(err.response.data));
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
    return promise;
};

const AddStudents = (studentsPromise, groups, setReload) => {
    studentsPromise.then(records => {
        let students = records.map(record => {
            let group_id = groups.filter(g => g.group_name === record.Группа).map(g => g.id)[0];
            let student = {
                surname: record.Фамилия,
                name: record.Имя,
                patronymic: record.Отчество,
                email: record.Почта,
                group_id: group_id
            };
            return student;
        }).filter(s => s.group_id !== (null || undefined));
        return students;
    }).then(loadedStudents => {
        let url = '/api/admin/add_students';
        axios.post(url, loadedStudents)
            .then(res => res.data)
            .then(studentsIds => {
                alert(`Студенты c ids = [${studentsIds}] успешно добавлены или уже существуют!`);
                setReload(reload => reload + 1);
            })
            .catch(err => alert(err.response.data));
    }).catch(err => alert(err.message));
};

const DelStudent = (studentId, setReload) => {
    let url = `/api/admin/del_student/${studentId}`;
    axios.delete(url)
        .then(res => res.data)
        .then(studentId => {
            alert(`Студент c id = ${studentId} успешно удален!`);
            setReload(reload => reload + 1);
        })
        .catch(err => alert(err.response.data));
};

export { AddGroup, AddStudent, AddStudents, DelGroup, DelStudent, ReadExcel }