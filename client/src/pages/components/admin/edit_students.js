import { React, useState, useMemo } from 'react';
import { Accordion } from "react-bootstrap";
import AccordionBody from 'react-bootstrap/esm/AccordionBody';
import AccordionHeader from 'react-bootstrap/esm/AccordionHeader';
import AccordionItem from 'react-bootstrap/esm/AccordionItem';
import AuthUserForm from '../common/auth_form';
import GroupSelector from '../common/group_selector';
import Filter from './filter';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBan, faMinus, faPlus, faPen } from '@fortawesome/free-solid-svg-icons';
import { AddGroup, AddStudent, AddStudents, DelGroup, DelStudent, ReadExcel, patchEmail } from './manager';
import { Sort, GetClassNameFor } from './sorter';

const EditStudent = (props) => {
    const [groupName, setGroupName] = useState('');
    const [surname, setSurname] = useState('');
    const [name, setName] = useState('');
    const [patronymic, setPatronymic] = useState('');
    const [email, setEmail] = useState('');
    const [filter, setFilter] = useState('');
    const [sortConfig, setSortConfig] = useState({ key: null, direction: null });
    const [selectedYear, selectedGroup, setSelectedGroup, groups, students, setReload, navigate] = props.params;
    const paramsPack = [surname, setSurname, name, setName, patronymic, setPatronymic, email, setEmail];
    const filteredStudents = useMemo(() => {
        let filteredStudents = [];
        if (filter.length > 0) {
            filteredStudents = students.filter(s => s.surname.toLowerCase().startsWith(filter.toLowerCase()));
        }
        else {
            filteredStudents = students;
        }
        return filteredStudents;
    }, [students, filter]);
    return (
        <div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="group" className="form-label">Группа:</label>
                </div>
                <div className="col-sm-8">
                    <input value={groupName} onChange={(e) => setGroupName(e.target.value)}
                        className="form-control" type="text" placeholder='Группа' />
                    <span className="input-group-btn">
                        <button className="btn btn-default" type="button" title="Добавить"
                            onClick={() => AddGroup(groupName, setGroupName, setReload, navigate)}>
                            <span style={{ "color": "green" }}>
                                <FontAwesomeIcon icon={faPlus}></FontAwesomeIcon>
                            </span>
                        </button>
                        <button className="btn btn-default" type="button" title="Удалить"
                            onClick={() => DelGroup(groups, groupName, setGroupName, setReload, navigate)}>
                            <span style={{ "color": "red" }}>
                                <FontAwesomeIcon icon={faMinus}></FontAwesomeIcon>
                            </span>
                        </button>
                    </span>
                </div>
            </div>
            <Accordion defaultActiveKey="0">
                <AccordionItem eventKey="0">
                    <AccordionHeader>Ввести студентов вручную</AccordionHeader>
                    <AccordionBody>
                        <AuthUserForm paramsPack={paramsPack} />
                        <div className="row mb-2">
                            <div className="col-sm-4">
                                <label htmlFor="group" className="form-label">Группа:</label>
                            </div>
                            <div className="col-sm-8">
                                <GroupSelector groups={[groups, selectedYear.id, selectedGroup, setSelectedGroup]} />
                            </div>
                        </div>
                        <div className="row mb-2">
                            <div className="col-sm-4"></div>
                            <div className="col-sm-8">
                                <button className="btn btn-default" type="button" title="Добавить"
                                    onClick={() => AddStudent(surname, setSurname, name, setName, patronymic, setPatronymic, email, setEmail, selectedGroup, setReload, navigate)}>
                                    <span style={{ "color": "green" }}>
                                        <FontAwesomeIcon icon={faPlus}></FontAwesomeIcon>
                                    </span>
                                </button>
                            </div>
                        </div>
                    </AccordionBody>
                </AccordionItem>
                <AccordionItem eventKey="1">
                    <AccordionHeader>Загрузить студентов из файла</AccordionHeader>
                    <AccordionBody>
                        <label htmlFor="import" className="btn btn-outline-primary">Загрузить студентов</label>
                        <input id="import" type="file" style={{ "visibility": "hidden", "maxWidth": "0" }}
                            onChange={(e) => {
                                let studentsPromise = ReadExcel(e);
                                AddStudents(studentsPromise, groups, setReload, navigate);
                            }} />
                    </AccordionBody>
                </AccordionItem>
                <AccordionItem eventKey="2">
                    <AccordionHeader>Просмотреть студентов</AccordionHeader>
                    <AccordionBody>
                        <Filter filter={filter} setFilter={setFilter} />
                        <div className="container-fluid">
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th scope="col">№</th>
                                        <th scope="col">
                                            <button className={GetClassNameFor('surname', sortConfig)}
                                                onClick={() => Sort(filteredStudents, 'surname', sortConfig, setSortConfig)}>
                                                Фамилия
                                            </button>
                                        </th>
                                        <th scope="col">
                                            <button className={GetClassNameFor('name', sortConfig)}
                                                onClick={() => Sort(filteredStudents, 'name', sortConfig, setSortConfig)}>
                                                Имя
                                            </button>
                                        </th>
                                        <th scope="col">
                                            <button onClick={() => { }}>
                                                Отчество
                                            </button>
                                        </th>
                                        <th scope="col" className='email'>
                                            <button className={ GetClassNameFor('email', sortConfig) }
                                                onClick={() => Sort(filteredStudents, 'email', sortConfig, setSortConfig)}>
                                                Эл.почта
                                            </button>
                                        </th>
                                        <th scope="col" className='email'></th>
                                        <th scope="col">
                                            <button className={ GetClassNameFor('group_id', sortConfig) }
                                                onClick={() => Sort(filteredStudents, 'group_id', sortConfig, setSortConfig)}>
                                                Группа
                                            </button>
                                        </th>
                                        <th scope="col"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredStudents.map((student, idx) => (
                                        <tr key={student.id}>
                                            <td>{idx + 1}</td>
                                            <td>{student.surname}</td>
                                            <td>{student.name}</td>
                                            <td>{student.patronymic}</td>
                                            <td className='email'>{student.email}</td>
                                            <td className='email'>
                                                <button className="btn btn-default" type="button" title="Исправить email"
                                                    onClick={() => {
                                                        let email = prompt('Введите ответ: ');
                                                        if (![null, ''].includes(email)) { patchEmail(student.id, email, setReload, navigate) }
                                                    }}>
                                                    <span style={{ "color": "#c9643b" }}>
                                                        <FontAwesomeIcon icon={faPen}></FontAwesomeIcon>
                                                    </span>
                                                </button>
                                            </td>
                                            <td>{groups.filter(g => g.id === student.group_id).map(g => g.group_name)[0]}</td>
                                            <td>
                                                <button className="btn btn-default" type="button" title="Удалить"
                                                    onClick={() => {
                                                        let yes = window.confirm("Удалить студента?");
                                                        if (yes) { DelStudent(student.id, setReload, navigate) }
                                                    }}>
                                                    <span style={{ "color": "red" }}>
                                                        <FontAwesomeIcon icon={faBan}></FontAwesomeIcon>
                                                    </span>
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </AccordionBody>
                </AccordionItem>
            </Accordion>
        </div >
    );
}

export default EditStudent;