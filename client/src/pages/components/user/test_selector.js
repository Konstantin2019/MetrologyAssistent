import { React, useEffect } from 'react';

const TestSelector = (props) => {
    const [tests, selectedTest, setSelectedTest] = props.tests;
    useEffect(() => { }, [tests]);
    return (
        <div className="input-group">
            <select className="form-control" value={selectedTest.test_name}
                onChange={(e) => {
                    let index = e.target.selectedIndex;
                    let elem = e.target.childNodes[index];
                    let test_id = parseInt(elem.id);
                    setSelectedTest({
                        id: test_id,
                        test_name: e.target.value,
                        test_view: elem.textContent
                    });
                }}>
                {tests.map((test) => (
                    <option key={test.id} value={test.test_name}>{test.test_view}</option>
                ))}
            </select>
        </div>
    );
}

export default TestSelector;