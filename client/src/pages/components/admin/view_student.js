import { React, useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye } from '@fortawesome/free-solid-svg-icons';
import GetData from '../../../local_storage';

const ViewStudent = ({ students }) => {
    const navigate = useNavigate();
    const [tests] = useState(GetData().tests);
    useEffect(() => { console.log(students) }, [students]);
    return (
        <table className="table">
            <thead>
                <tr>
                    <th scope="col">№</th>
                    <th scope="col">Фамилия</th>
                    <th scope="col">Имя</th>
                    <th scope="col">Отчество</th>
                    <th scope="col">Результат РК1</th>
                    <th scope="col">Результат РК2</th>
                    <th scope="col">Результат Зачёта</th>
                </tr>
            </thead>
            <tbody>
                {students.map((student, idx) => (
                    <tr key={student.id}>
                        <td>{idx + 1}</td>
                        <td>{student.surname}</td>
                        <td>{student.name}</td>
                        <td>{student.patronymic}</td>
                        <td>
                            <button className="btn btn-default" type="button" title="Просмотреть"
                                onClick={() => navigate(`/admin_panel/rk1/${student.id}`,
                                    {
                                        state: {
                                            studentId: student.id,
                                            surname: student.surname,
                                            name: student.name,
                                            patronymic: student.patronymic,
                                            test_name: tests[0].test_name,
                                            test_view: tests[0].test_view
                                        }
                                    })}>
                                <span style={{ "color": "purple" }}>
                                    <FontAwesomeIcon icon={faEye}></FontAwesomeIcon>
                                </span>
                            </button>
                            <span style={{ "marginLeft": "5%" }}>{student.rk1_score}</span>
                        </td>
                        <td>
                            <button className="btn btn-default" type="button" title="Просмотреть"
                                onClick={() => navigate(`/admin_panel/rk2/${student.id}`,
                                    {
                                        state: {
                                            studentId: student.id,
                                            surname: student.surname,
                                            name: student.name,
                                            patronymic: student.patronymic,
                                            test_name: tests[1].test_name,
                                            test_view: tests[1].test_view
                                        }
                                    })} >
                                <span style={{ color: "purple" }}>
                                    <FontAwesomeIcon icon={faEye}></FontAwesomeIcon>
                                </span>
                            </button>
                            <span style={{ "marginLeft": "5%" }}>{student.rk2_score}</span>
                        </td>
                        <td>
                            <button className="btn btn-default" type="button" title="Просмотреть"
                                onClick={() => navigate(`/admin_panel/test/${student.id}`,
                                    {
                                        state: {
                                            studentId: student.id,
                                            surname: student.surname,
                                            name: student.name,
                                            patronymic: student.patronymic,
                                            test_name: tests[2].test_name,
                                            test_view: tests[2].test_view
                                        }
                                    })} >
                                <span style={{ color: "purple" }}>
                                    <FontAwesomeIcon icon={faEye}></FontAwesomeIcon>
                                </span>
                            </button>
                            <span style={{ "marginLeft": "5%" }}>{student.test_score}</span>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export default ViewStudent;