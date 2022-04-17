import React from 'react';
import AuthUserComponent from './components/user/auth_component';

const UserAuth = () => {
    return (
        <div className="page">
            <div className="container">
                <div className="container-auth">
                    <h2>Аутентификация</h2>
                    <AuthUserComponent />
                </div>
            </div>
        </div>
    );
}

export default UserAuth;