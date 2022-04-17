import { React, useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

const AdminAuth = () => {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    function Authorize() {
        let url = '/api/admin_auth';
        let user = {
            login: login,
            password: password
        };
        axios.post(url, user)
            .then(_ => {
                alert("Успешная авторизация!");
                navigate('/admin_panel');
            })
            .catch(err => alert(err.response.data));
    };
    return (
        <div className="page">
            <div className="container">
                <div className="container-auth">
                    <h2>Админка</h2>
                    <form method="POST" onSubmit={(e) => {
                        Authorize();
                        e.preventDefault();
                    }}>
                        <div className="row mb-2">
                            <div className="col-sm-4">
                                <label htmlFor="login">Логин:&nbsp;&nbsp;</label>
                            </div>
                            <div className="col-sm-8">
                                <input value={login} className="form-control" type="text" placeholder="Логин"
                                    onChange={(e) => setLogin(e.target.value)} />
                            </div>
                        </div>
                        <div className="row mb-2">
                            <div className="col-sm-4">
                                <label htmlFor="password">Пароль:</label>
                            </div>
                            <div className="col-sm-8">
                                <input value={password} className="form-control" type="password" placeholder="Пароль"
                                    onChange={(e) => setPassword(e.target.value)} />
                            </div>
                        </div>
                        <div className="row justify-content-center">
                            <input className="btn btn-primary" id="submit" name="submit" type="submit" value="Подтвердить" />
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default AdminAuth;