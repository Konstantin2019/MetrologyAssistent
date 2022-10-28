import { createSlice } from "@reduxjs/toolkit";
import { fetchAll } from "../thunks/fetch";

const studentReducer = createSlice({
    name: "students",
    initialState: { students: [], studentError: null },
    reducers: {},
    extraReducers: {
        [fetchAll.fulfilled]: (state, { payload }) => {
            const fetchedStudents = payload['students'].map(json => JSON.parse(json));
            state.students = [...fetchedStudents];
        },
        [fetchAll.rejected]: (state, { message }) => {
            state.studentError = message;
        }
    }
});

export default studentReducer.reducer