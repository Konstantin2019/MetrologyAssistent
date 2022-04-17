import { React } from 'react';
import GroupSelector from '../common/group_selector';
import TestSelector from './test_selector';
import TeacherSelector from './teacher_selector';

const TestSelectForm = (props) => {
    const [selectedYear, selectedGroup, setSelectedGroup, selectedTest, setSelectedTest, selectedTeacher, setSelectedTeacher, groups, tests, teachers] = props.paramsPack;
    return (
        <div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="group" className="form-label">Группа:</label>
                </div>
                <div className="col-sm-8">
                    <GroupSelector groups={[groups, selectedYear.id, selectedGroup, setSelectedGroup]} />
                </div>
            </div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="group" className="form-label">РКонтроль:</label>
                </div>
                <div className="col-sm-8">
                    <TestSelector tests={[tests, selectedTest, setSelectedTest]} />
                </div>
            </div>
            <div className="row mb-2">
                <div className="col-sm-4">
                    <label htmlFor="group" className="form-label">Преподаватель:</label>
                </div>
                <div className="col-sm-8">
                    <TeacherSelector teachers={[teachers, selectedTeacher, setSelectedTeacher]} />
                </div>
            </div>
        </div>);
}

export default TestSelectForm;