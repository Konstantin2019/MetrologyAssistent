import { React, useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { DelQuestions, patchAnswer, patchScore } from "./manager";

const ViewQuestion = () => {
    const { state } = useLocation();
    const { studentId, surname, name, patronymic, test_name, test_view } = state;
    const [questions, setQuestions] = useState([]);
    const [reload, setReload] = useState(0);
    const navigate = useNavigate();
    useEffect(() => {
        let url = `/api/admin/view_student/${studentId}`;
        let token = sessionStorage.getItem('token');
        axios.get(url, { params: { rk: test_name, token: token } })
            .then(res => res.data)
            .then(data => data.map(json => JSON.parse(json)))
            .then(questions => questions.sort((q1, q2) => q1.index > q2.index ? 1 : -1))
            .then(sortedQuestions => setQuestions([...sortedQuestions]))
            .catch(err => {
                if (err.response.status === 401) { navigate('/admin_auth') }
                else { alert(err.response.data) }
            });
    }, [studentId, test_name, reload, navigate]);
    return (
        <div className="container" style={{ "marginTop": "1%", "marginBottom": "1%" }}>
            <div className="container-fluid">
                <span style={{ "fontSize": "25px", "color": "cornflowerblue" }}>
                    <b>{`${surname} ${name} ${patronymic} - ${test_view}`}
                    </b>
                </span>
                <table id={studentId} className="table">
                    <thead>
                        <tr>
                            <th scope="col">№</th>
                            <th scope="col">Вопрос</th>
                            <th scope="col">Ответ студента</th>
                            <th scope="col"></th>
                            <th scope="col">Правильный ответ</th>
                            <th scope="col">Балл</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {questions.map(question => (
                            <tr key={question.id}>
                                <td>{question.index}</td>
                                <td style={{ "textAlign": "justify" }}>{question.question}</td>
                                <td>{question.student_answer}</td>
                                <td>
                                    <button className="btn btn-default" type="button" title="Исправить ответ"
                                        onClick={() => {
                                            let answer = prompt('Введите ответ: ');
                                            if (![null, ''].includes(answer)) { patchAnswer(question.id, answer, test_name, setReload) }
                                        }}>
                                        <span style={{ "color": "#c9643b" }}>
                                            <FontAwesomeIcon icon={faPen}></FontAwesomeIcon>
                                        </span>
                                    </button>
                                </td>
                                <td>{question.correct_answer}</td>
                                <td>{question.score}</td>
                                <td>
                                    <button className="btn btn-default" type="button" title="Исправить балл"
                                        onClick={() => {
                                            let score = parseInt(prompt('Введите балл: '));
                                            if (!isNaN(score)) { patchScore(question.id, score, test_name, setReload) }
                                        }}>
                                        <span style={{ "color": "#c9643b" }}>
                                            <FontAwesomeIcon icon={faPen}></FontAwesomeIcon>
                                        </span>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <p>
                    <button className="btn btn-outline-danger" onClick={() => {
                        let yes = window.confirm("Вы уверены, что хотите сбросить вопросы?");
                        if (yes) { DelQuestions(studentId, test_name, setReload) }
                    }}>
                        Сбросить данные
                    </button>
                </p>
                <p>
                    <a className="btn btn-primary btn-lg" role="button" href="/admin_panel">
                        Назад
                    </a>
                </p>
            </div>
        </div >
    );
}

export default ViewQuestion;