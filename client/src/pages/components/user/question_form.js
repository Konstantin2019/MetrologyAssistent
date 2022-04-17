import { React, useEffect, useState } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from 'axios';

const QuestionForm = ({ url, question, images }) => {
    const [image, setImage] = useState(null);
    const [answer, setAnswer] = useState('');
    const sendAnswer = () => {
        let answerInfo = {
            question_id: question.id,
            index: question.index,
            student_answer: answer
        };
        axios.post(url, answerInfo)
            .then(res => res.data)
            .then(info => alert(info))
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
                    <input value={answer} className="form-control"
                        type="text" placeholder="Ответ"
                        onChange={(e) => setAnswer(e.target.value)} />
                </Col>
            </Row>
            <Row className="row justify-content-center">
                <input className="btn btn-primary" type="submit" value="Отправить" />
            </Row>
        </form>
    );
}

export default QuestionForm;