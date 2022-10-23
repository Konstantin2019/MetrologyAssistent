import { React, useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import Row from 'react-bootstrap/Row';
import PaginationComponent from './components/user/pagination';
import QuestionsComponent from './components/user/questions';
import StudentLabel from './components/user/student_label';
import axios from 'axios';
import { trackPromise } from 'react-promise-tracker';

const UserTest = () => {
    const { state } = useLocation();
    const { surname, name, patronymic, group, test, teacher } = state;
    const dbQuestions = useRef([]);
    const timerId = useRef(null);
    const images = useRef([]);
    const [url] = useState('/api/user' + window.location.pathname);
    const [remainingTime, setRemainingTime] = useState(60);
    const [currentPage, setCurrentPage] = useState(0);
    const [questionsPerPage] = useState(1);
    const [totalQuestions, setTotalQuestions] = useState(5);
    const paginate = page => setCurrentPage(page);
    const prev = () => setCurrentPage(page => page > 1 ? page - 1 : page);
    const next = total => setCurrentPage(page => page < total ? page + 1 : page);
    const navigate = useNavigate();
    const finish = useCallback(
        () => {
            axios.post(url, { status: 'finish' })
                .then(_ => {
                    alert("Рубежный контроль завершён!");
                    navigate('/');
                })
                .catch(err => alert(err.response.data))
        }, [url, navigate]);
    const setTime = useCallback(
        (startTime, interval) => {
            if (startTime !== (undefined || null) && interval !== (undefined || null)) {
                let timeLeft = Math.round((new Date() - new Date(startTime)) / 60000); //в мин
                let remainingTime = interval - timeLeft;
                if (remainingTime >= 0) { setRemainingTime(remainingTime) }
                else { finish() }
            };
        }, [finish]);
    useEffect(() => {
        const CancelToken = axios.CancelToken;
        const source = CancelToken.source();
        trackPromise(
            axios.get(url, { cancelToken: source.token })
                .then(res => res.data)
                .then(data => {
                    let startTime = data['start'];
                    let interval = data['duration'];
                    let questions = data['questions'].map(json => JSON.parse(json));
                    if (questions.length > 0) {
                        dbQuestions.current = questions.sort((q1, q2) => q1.index > q2.index ? 1 : -1);
                        for (let i = 0; i < questions.length; i++) { images.current.push(null) }
                        setTotalQuestions(dbQuestions.current.length);
                        setCurrentPage(1);
                        setTime(startTime, interval);
                        let delay = 60 * 1000;
                        timerId.current = setInterval(() => setTime(startTime, interval), delay);
                    }
                })
                .catch(err => {
                    alert(err.response.data);
                    navigate('/');
                })
        );
        return () => {
            source.cancel();
            if (timerId !== null) { clearInterval(timerId.current) };
        };
    }, [dbQuestions, images, url, navigate, setTime]);
    const currentQuestions = useMemo(
        () => {
            let lastIdx = currentPage * questionsPerPage;
            let firstIdx = lastIdx - questionsPerPage;
            let currentQuestions = dbQuestions.current.slice(firstIdx, lastIdx);
            return currentQuestions;
        }, [dbQuestions, currentPage, questionsPerPage]);
    return (
        <section>
            <StudentLabel params={[surname, name, patronymic, group, test, teacher, remainingTime]} />
            <QuestionsComponent url={url} questions={currentQuestions} images={images} />
            <div className="container">
                <Row>
                    <PaginationComponent navigate={[questionsPerPage, totalQuestions, paginate, prev, next]} />
                </Row>
                <Row className="row justify-content-center">
                    <input className="btn btn-success" value="Завершить"
                        style={{ "maxWidth": "50%" }}
                        onClick={() => {
                            let yes = window.confirm("Вы уверены, что хотите завершить?");
                            if (yes) { finish() }
                        }}
                    />
                </Row>
            </div>
        </section >
    );
}

export default UserTest;