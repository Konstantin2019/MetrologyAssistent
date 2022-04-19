import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const StudentLabel = (props) => {
    const [surname, name, patronymic, group, test, teacher, remainingTime] = props.params;
    return (
        <div className="container" style={{ "width": "50%", "marginTop": "1%" }}>
            <Row className="student-info">
                <Col className='student-label'>
                    <label>ФИО:</label>
                </Col>
                <Col className="student-label">
                    <label>{`${surname} ${name} ${patronymic}`}</label>
                </Col>
            </Row>
            <Row className="student-info">
                <Col className="student-label">
                    <label>Группа:</label>
                </Col>
                <Col className="student-label">
                    <label>{group}</label>
                </Col>
            </Row>
            <Row className="student-info">
                <Col className="student-label">
                    <label>РК:</label>
                </Col>
                <Col className="student-label">
                    <label>{test}</label>
                </Col>
            </Row>
            <Row className="student-info">
                <Col className="student-label">
                    <label>Преподаватель:</label>
                </Col>
                <Col className="student-label">
                    <label>{teacher}</label>
                </Col>
            </Row>
            <Row className="timer-label">
                <label>Осталось {remainingTime} мин</label>
            </Row>
        </div>
    )
}

export default StudentLabel;