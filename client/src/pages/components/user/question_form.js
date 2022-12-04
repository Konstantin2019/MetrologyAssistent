import { React, useEffect, useState } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from 'axios';

const QuestionForm = ({ url, question, images }) => {
    const [image, setImage] = useState(null);
    const [answer, setAnswer] = useState(null);
    const sendAnswer = () => {
        let answerInfo = {
            question_id: question.id,
            index: question.index,
            student_answer: answer
        };
        axios.post(url, answerInfo)
            .then(res => alert(res.data))
            .catch(err => alert(err.response.data));
    };
    useEffect(() => {
        let idx = question.index - 1
        if (images.current[idx] === null) {
            axios.get(question.image_url, { responseType: "blob" })
                .then(res => {
                    let img = URL.createObjectURL(res.data);
                    setImage(img);
                    images.current[idx] = img;
                })
                .catch(err => alert(err));
        }
        else {
            let img = images.current[idx];
            setImage(img);
        }
    }, [question, images]);
    return (
        <form method="POST" style={{ "padding": "0%" }}
            onSubmit={(e) => {
                sendAnswer();
                e.preventDefault();
            }}>
            <img src={image} width={'30%'} height={'30%'} alt={'task'}></img>
            <Row>
                <Col style={{ "maxWidth": "2%" }}>
                    <span>{question.index}</span>
                </Col>
                <Col style={{ "textAlign": "justify" }}>
                    <span>{question.question}</span>
                    <Row>
                        <Col>
                            <input value={answer} className="form-control"
                                type="text" placeholder="Ответ"
                                onChange={(e) => setAnswer(e.target.value)} />
                        </Col>
                        <Col style={{ "maxWidth": "17%" }}>
                            <label htmlFor="import" className="btn btn-outline-primary">Прикрепить решение</label>
                            <input id="import" type="file" style={{ "visibility": "hidden", "maxWidth": "0" }}
                                onChange={(e) => {
                                    const file = e.target.files[0];
                                    const ext = file.name.split('.')[1];
                                    if (ext === 'jpg' || ext === 'jpeg') {
                                        const image = new Promise((resolve, reject) => {
                                            const reader = new FileReader();
                                            reader.readAsBinaryString(file);
                                            reader.onload = (e) => resolve(e.target.result);
                                            reader.onerror = (e) => reject(e);
                                        });
                                        image.then(blob => {
                                            const payload = {
                                                question_id: question.id,
                                                answer_image: blob
                                            };
                                            axios.post(url, payload)
                                                .then(res => alert(res.data))
                                                .catch(err => alert(err));
                                        });
                                    }
                                }} />
                        </Col>
                    </Row>
                </Col>
            </Row>
            <Row className="row justify-content-center">
                <input className="btn btn-primary" type="submit" value="Отправить" />
            </Row>
        </form>
    );
}

export default QuestionForm;