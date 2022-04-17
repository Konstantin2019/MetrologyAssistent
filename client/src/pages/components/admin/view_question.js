import { React, useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';

const ViewQuestion = () => {
    const { state } = useLocation();
    const { studentId, surname, name, patronymic, test_name, test_view } = state;
    const [questions, setQuestions] = useState([]);
    const [reload, setReload] = useState(0);
    useEffect(() => {
        let url = `/api/admin/view_student/${studentId}`;
        axios.get(url, { params: { rk: test_name } })
            .then(res => res.data)
            .then(data => data.map(json => JSON.parse(json)))
            .then(questions => questions.sort((q1, q2) => q1.index > q2.index ? 1 : -1))
            .then(sortedQuestions => setQuestions([...sortedQuestions]))
            .catch(err => alert(err.response.data));
    }, [studentId, test_name, reload]);
    const patchScore = (questionId, score) => {
        let url = `/api/admin/patch_question/${questionId}`;
        let patch = {
            rk: test_name,
            question_score: score
        };
        axios.post(url, patch)
            .then(_ => { })
            .catch(err => alert(err.response.data))
            .finally(_ => setReload(reload => reload + 1));
    };
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
                                <td>{question.correct_answer}</td>
                                <td>{question.score}</td>
                                <td>
                                    <button className="btn btn-default" type="button" title="Исправить балл"
                                        onClick={() => {
                                            let score = parseInt(prompt('Введите балл: '));
                                            if (!isNaN(score)) { patchScore(question.id, score) }
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
                <p className="text-center wow pulse">
                    <a className="btn btn-primary btn-lg" role="button" href="/admin_panel">
                        Назад
                    </a>
                </p>
            </div>
        </div >
    );
}

export default ViewQuestion;