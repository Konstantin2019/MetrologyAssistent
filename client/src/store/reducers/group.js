import { createSlice } from "@reduxjs/toolkit";
import { fetchAll } from "../thunks/fetch";

const groupReducer = createSlice({
    name: "groups",
    initialState: { groups: [], selectedGroup: null, groupError: null },
    reducers: {
        changeGroup(state, { payload }) { state.selectedGroup = payload }
    },
    extraReducers: {
        [fetchAll.fulfilled]: (state, { payload }) => {
            const fetchedGroups = payload['groups'].map(json => JSON.parse(json));
            state.groups = [...fetchedGroups];
        },
        [fetchAll.rejected]: (state, { message }) => {
            state.groupError = message;
        }
    }
});

export const { changeGroup } = yearReducer.actions;

export default groupReducer.reducer