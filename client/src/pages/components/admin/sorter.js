const Sort = (students, key, sortConfig, setSortConfig) => {
    let direction = 'ascending';
    if (sortConfig.key === key
        && sortConfig.direction === direction) { direction = 'descending' }
    setSortConfig({ key, direction });
    if (direction === 'ascending') {
        students.sort((s1, s2) => s1[key] > s2[key] ? 1 : -1)
    }
    if (direction === 'descending') {
        students.sort((s1, s2) => s1[key] < s2[key] ? 1 : -1)
    }
};

const GetClassNameFor = (key, sortConfig) => sortConfig.key === key ? sortConfig.direction : null;

export { Sort, GetClassNameFor }