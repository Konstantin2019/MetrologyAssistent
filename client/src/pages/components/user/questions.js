import { React, useEffect } from 'react';
import QuestionForm from './question_form';

const QuestionsComponent = ({ url, questions, images }) => {
    useEffect(() => { }, [questions]);
    return (
        <div className="container">
            {questions.map(question => (
                <div className="container-fluid" key={question.id}>
                    <QuestionForm url={url} question={question} images={images} />
                </div>
            ))}
        </div>
    );
}

export default QuestionsComponent;