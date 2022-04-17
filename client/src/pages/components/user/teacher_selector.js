import { React, useEffect } from 'react';

const TeacherSelector = (props) => {
    const [teachers, selectedTeacher, setSelectedTeacher] = props.teachers;
    useEffect(() => { }, [teachers]);
    return (
        <div className="input-group">
            <select className="form-control" value={selectedTeacher.teacher_name}
                onChange={(e) => {
                    let index = e.target.selectedIndex;
                    let elem = e.target.childNodes[index];
                    let teacher_id = parseInt(elem.id);
                    setSelectedTeacher({
                        id: teacher_id,
                        teacher_name: e.target.value,
                        teacher_view: elem.textContent
                    });
                }}>
                {teachers.map((teacher) => (
                    <option key={teacher.id} value={teacher.teacher_name}>{teacher.teacher_view}</option>
                ))}
            </select>
        </div>
    );
}

export default TeacherSelector;