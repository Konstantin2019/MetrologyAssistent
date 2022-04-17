import { React } from 'react';

const Filter = ({ filter, setFilter }) => {
    return (
        <div className="row mb-2">
            <div className="col">
                <input value={filter} className="form-control" type="text" placeholder='Фильтр'
                    onChange={(e) => setFilter(e.target.value)} />
            </div>
        </div>
    );
}

export default Filter;