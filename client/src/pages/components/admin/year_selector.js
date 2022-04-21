import { React, useEffect } from 'react';

const YearSelector = (props) => {
    const [years, selectedYear, setSelectedYear] = props.years;
    useEffect(() => { }, [years]);
    return (
        <div className="input-group">
            <select className="form-control" value={selectedYear.year_name}
                onChange={(e) => {
                    let index = e.target.selectedIndex;
                    let elem = e.target.childNodes[index];
                    let year_id = parseInt(elem.id);
                    let year = {
                        id: year_id,
                        year_name: e.target.value
                    }
                    setSelectedYear(year);
                }}>
                {years.map((year) => (
                    <option id={year.id} key={year.id} value={year.year_name}>{year.year_name}</option>
                ))}
            </select>
        </div>
    );
}

export default YearSelector;