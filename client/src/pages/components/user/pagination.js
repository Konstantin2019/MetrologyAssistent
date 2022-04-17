import React from 'react';

const PaginationComponent = (props) => {
    const [questionsPerPage, totalQuestions, paginate, prev, next] = props.navigate;
    const pages = [];
    for (let i = 1; i <= Math.ceil(totalQuestions / questionsPerPage); i++) {
        pages.push(i)
    }
    return (
        <div className='pagination justify-content-center'>
            <li className="page-item">
                <a href="#!" className="page-link" onClick={(e) => {
                    prev();
                    e.preventDefault();
                }}>Назад</a>
            </li>
            {
                pages.map(num => (
                    <li className='page-item' key={num}>
                        <a href="#!" className='page-link' onClick={(e) => {
                            paginate(num);
                            e.preventDefault();
                        }}>{num}</a>
                    </li>
                ))
            }
            <li className="page-item">
                <a href="#!" className="page-link" onClick={(e) => {
                    next(pages.length);
                    e.preventDefault();
                }}>Вперед</a>
            </li>
        </div>
    );
}

export default PaginationComponent;