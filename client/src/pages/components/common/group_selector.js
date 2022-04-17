import { React, useEffect } from 'react';

const GroupSelector = (props) => {
    const [groups, selectedYearId, selectedGroup, setSelectedGroup] = props.groups;
    useEffect(() => { }, [groups]);
    return (
        <div className="input-group">
            <select className="form-control" value={selectedGroup.group_name}
                onChange={(e) => {
                    let index = e.target.selectedIndex;
                    let elem = e.target.childNodes[index];
                    let group_id = parseInt(elem.id);
                    setSelectedGroup({
                        group_name: e.target.value,
                        id: group_id,
                        year_id: selectedYearId
                    })
                }}>
                {groups.map((group) => (
                    <option id={group.id} key={group.id} value={group.group_name}>{group.group_name}</option>
                ))}
            </select>
        </div>
    );
}

export default GroupSelector;