import React from 'react';

const AuthUserForm = (props) => {
    const [surname, setSurname, name, setName, patronymic, setPatronymic, email, setEmail] = props.paramsPack;
    return (
        <div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="surname" className="form-label">Фамилия:</label>
                </div>
                <div className="col-sm-8">
                    <input value={surname} className="form-control" type="text" placeholder='Фамилия'
                        onChange={(e) => setSurname(e.target.value)} />
                </div>
            </div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="name" className="form-label">Имя:</label>
                </div>
                <div className="col-sm-8">
                    <input value={name} className="form-control" type="text" placeholder="Имя"
                        onChange={(e) => setName(e.target.value)} />
                </div>
            </div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="patronymic" className="form-label">Отчество:</label>
                </div>
                <div className="col-sm-8">
                    <input value={patronymic} className="form-control" type="text" placeholder="Отчество"
                        onChange={(e) => setPatronymic(e.target.value)} />
                </div>
            </div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="email" className="form-label">Эл.почта:</label>
                </div>
                <div className="col-sm-8">
                    <input value={email} className="form-control" type="email" placeholder="Электронная почта"
                        onChange={(e) => setEmail(e.target.value)} />
                </div>
            </div>
        </div>
    );
}

export default AuthUserForm;