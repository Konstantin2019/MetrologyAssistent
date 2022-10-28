import { createSlice } from "@reduxjs/toolkit";
import { fetchAll } from "../thunks/fetch";

const yearReducer = createSlice({
    name: "years",
    initialState: { years: [], selectedYear: null, yearError: null },
    reducers: {
        changeYear(state, { payload }) { state.selectedYear = payload }
    },
    extraReducers: {
        [fetchAll.fulfilled]: (state, { payload }) => {
            const fetchedYears = payload['years'].map(json => JSON.parse(json));
            state.years = [...fetchedYears];
        },
        [fetchAll.rejected]: (state, { message }) => {
            state.yearError = message;
        }
    }
});

export const { changeYear } = yearReducer.actions;

export default yearReducer.reducer