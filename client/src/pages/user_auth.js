import React from 'react';

const UserAuth = () => {
    const [surname, setSurname] = useState('');
    const [name, setName] = useState('');
    const [patronymic, setPatronymic] = useState('');
    const [email, setEmail] = useState('');
    const [groups, setGroups] = useState([]);
    const [tests, setTests] = useState([]);
    const [teachers, setTeachers] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState({ group_name: '', id: 0, year_id: 0 })
    const [selectedYear, setSelectedYear] = useState({ id: 0, year_name: '' });
    const [selectedTest, setSelectedTest] = useState({ id: 0, test_name: '', test_view: '' });
    const [selectedTeacher, setSelectedTeacher] = useState({ id: 0, teacher_name: '', teacher_view: '' });
    const navigate = useNavigate();
    useEffect(() => {
        let url = '/api/for_user_auth';
        axios.get(url)
            .then(res => res.data)
            .then(data => {
                let year = data['year']
                let groups = data['groups'].map(json => JSON.parse(json));
                let teachers = data['teachers'].map(json => JSON.parse(json));
                let tests = data['tests'].map(json => JSON.parse(json));
                if (year !== (undefined || null)) {
                    setSelectedYear(year);
                }
                if (groups.length > 0) {
                    setGroups([...groups]);
                    setSelectedGroup(groups[0]);
                };
                if (tests.length > 0 && teachers.length > 0) {
                    setTests([...tests]);
                    setSelectedTest(tests[0]);
                    setTeachers([...teachers]);
                    setSelectedTeacher(teachers[0]);
                }
            })
            .catch(err => alert(err.response.data));
    }, []);
    const Auth = () => {
        let url = '/api/user_auth';
        axios.post(url, { email: email })
            .then(res => res.data)
            .then(studentId => navigate(`/test/${studentId}/${selectedTest.test_name}/${selectedTeacher.teacher_name}`,
                {
                    state: {
                        surname: surname,
                        name: name,
                        patronymic: patronymic,
                        group: selectedGroup.group_name,
                        test: selectedTest.test_view,
                        teacher: selectedTeacher.teacher_view
                    }
                }))
            .catch(err => alert(err.response.data));
    }
    const paramsPack1 = [surname, setSurname, name, setName, patronymic, setPatronymic, email, setEmail];
    const paramsPack2 = [selectedYear, selectedGroup, setSelectedGroup,
                         selectedTest, setSelectedTest, selectedTeacher, setSelectedTeacher, 
                         groups, tests, teachers];
    return (
        <div className="page">
            <div className="container">
                <div className="container-auth">
                    <h2>Аутентификация</h2>
                    <form method="POST" onSubmit={(e) => {
                        Auth();
                        e.preventDefault();
                    }}>
                        <AuthUserForm paramsPack={paramsPack1} />
                        <TestSelectForm paramsPack={paramsPack2} />
                        <div className="row justify-content-center">
                            <input className="btn btn-primary" type="submit" value="Подтвердить" />
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default UserAuth;