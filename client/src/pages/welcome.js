import React from 'react';

const Welcome = () => {
    return (
        <div className="page">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="container-fluid">
                        <div className="col-sm-12">
                            <h1 className="text-center">Тестирование по метрологии</h1>
                            <p className="text-justify">Ресурс предназначен для тестирования по метрологии в рамках курса
                                "Метрология, стандартизация и взаимозаменяемость"</p>
                            <p className="text-center wow pulse">
                                <a className="btn btn-primary btn-lg" role="button" href="/user_auth">
                                    Начать
                                </a>
                            </p>
                            <a href="/admin_auth">Преподавателям</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Welcome;