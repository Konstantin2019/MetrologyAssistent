import React from 'react';
import Welcome from './pages/welcome';
import UserAuth from './pages/user_auth';
import AdminAuth from './pages/admin_auth';
import UserTest from './pages/user_test';
import AdminPanel from './pages/admin_panel';
import ViewQuestion from './pages/components/admin/view_question';
import './styles/App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/user_auth" element={<UserAuth />} />
        <Route path="/admin_auth" element={<AdminAuth />} />
        <Route path="/admin_panel" element={<AdminPanel />} />
        <Route path="/test/:studentId/:testType/:teacher" element={<UserTest />} />
        <Route path="/admin_panel/:testType/:studentId" element={<ViewQuestion />} />
      </Routes>
    </Router>
  );
}

export default App;