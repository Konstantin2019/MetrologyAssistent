import { React, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye } from '@fortawesome/free-solid-svg-icons';

const ViewStudent = ({ students, tests }) => {
    const navigate = useNavigate();
    useEffect(() => { }, [students]);
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
                                onClick={() => {
                                    let rk = tests[0];
                                    navigate(`/admin_panel/${rk.test_name}/${student.id}`,
                                        {
                                            state: {
                                                studentId: student.id,
                                                surname: student.surname,
                                                name: student.name,
                                                patronymic: student.patronymic,
                                                test_name: rk.test_name,
                                                test_view: rk.test_view
                                            }
                                        });
                                }}>
                                <span style={{ "color": "purple" }}>
                                    <FontAwesomeIcon icon={faEye}></FontAwesomeIcon>
                                </span>
                            </button>
                            <span style={{ "marginLeft": "5%" }}>{student.rk1_score}</span>
                        </td>
                        <td>
                            <button className="btn btn-default" type="button" title="Просмотреть"
                                onClick={() => {
                                    let rk = tests[1];
                                    navigate(`/admin_panel/${rk.test_name}/${student.id}`,
                                        {
                                            state: {
                                                studentId: student.id,
                                                surname: student.surname,
                                                name: student.name,
                                                patronymic: student.patronymic,
                                                test_name: rk.test_name,
                                                test_view: rk.test_view
                                            }
                                        });
                                }}>
                                <span style={{ color: "purple" }}>
                                    <FontAwesomeIcon icon={faEye}></FontAwesomeIcon>
                                </span>
                            </button>
                            <span style={{ "marginLeft": "5%" }}>{student.rk2_score}</span>
                        </td>
                        <td>
                            <button className="btn btn-default" type="button" title="Просмотреть"
                                onClick={() => {
                                    let rk = tests[2];
                                    navigate(`/admin_panel/${rk.test_name}/${student.id}`,
                                        {
                                            state: {
                                                studentId: student.id,
                                                surname: student.surname,
                                                name: student.name,
                                                patronymic: student.patronymic,
                                                test_name: rk.test_name,
                                                test_view: rk.test_view
                                            }
                                        });
                                }}>
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