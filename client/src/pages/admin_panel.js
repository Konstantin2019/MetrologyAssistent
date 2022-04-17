import { React, useState, useEffect, useRef, useMemo } from 'react';
import Tabs from 'react-bootstrap/Tabs';
import { Tab } from 'bootstrap';
import { useNavigate } from "react-router-dom";
import YearSelector from './components/admin/year_selector';
import GroupSelector from './components/common/group_selector';
import ViewStudent from './components/admin/view_student';
import EditStudent from './components/admin/edit_students';
import axios from 'axios';

const AdminPanel = () => {
    const [reload, setReload] = useState(0);
    const [dbYears, dbGroups, dbStudents] = [useRef([]), useRef([]), useRef([])];
    const [years, setYears] = useState([]);
    const [selectedYear, setSelectedYear] = useState({ id: 0, year_name: '' });
    const [selectedGroup, setSelectedGroup] = useState({ group_name: '', id: 0, year_id: 0 });
    const navigate = useNavigate();
    useEffect(() => {
        let url = '/api/admin';
        axios.get(url)
            .then(res => res.data)
            .then(data => {
                dbYears.current = data['years'].map(json => JSON.parse(json));
                dbGroups.current = data['groups'].map(json => JSON.parse(json));
                dbStudents.current = data['students'].map(json => JSON.parse(json));
                if (dbYears.current.length > 0) {
                    setYears([...dbYears.current]);
                    setSelectedYear(dbYears.current[0]);
                }
                if (dbGroups.current.length > 0) {
                    setSelectedGroup(dbGroups.current[0]);
                }
            })
            .catch(_ => navigate('/admin_auth'));
    }, [dbYears, dbGroups, dbStudents, reload, navigate]);
    const groups = useMemo(
        () => dbGroups.current.filter(g => g.year_id === selectedYear.id),
        [dbGroups, selectedYear]
    );
    const students = useMemo(
        () => dbStudents.current.filter(s => groups.map(g => g.id).includes(s.group_id)),
        [dbStudents, groups]
    );
    const currentStudents = useMemo(
        () => students
            .filter(s => s.group_id === selectedGroup.id)
            .sort((s1, s2) => s1.surname.toLowerCase() > s2.surname.toLowerCase() ? 1 : -1),
        [selectedGroup, students]
    );
    return (
        <Tabs defaultActiveKey="view" className="mb-3" style={{ "justifyContent": "center" }}>
            <Tab eventKey="view" title="Просмотреть">
                <div style={{ "marginTop": "1%", "marginBottom": "1%" }}>
                    <section>
                        <div className="container">
                            <div className="container-fluid">
                                <h1>Панель преподавателя</h1>
                                <div className="row">
                                    <div className="col-sm">
                                        <YearSelector years={[years, selectedYear, setSelectedYear]} />
                                    </div>
                                    <div className="col-sm">
                                        <GroupSelector groups={[groups, selectedYear.id, selectedGroup, setSelectedGroup]} />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                    <section id="content">
                        <div className="container">
                            <div className="container-fluid">
                                <ViewStudent students={currentStudents} />
                            </div>
                        </div>
                    </section>
                </div>
            </Tab>
            <Tab eventKey="edit" title="Редактировать">
                <div className="container">
                    <div className="container-fluid">
                        <EditStudent params={[selectedYear, selectedGroup, setSelectedGroup, groups, students, setReload]} />
                    </div>
                </div>
            </Tab>
        </Tabs>
    );
}

export default AdminPanel;