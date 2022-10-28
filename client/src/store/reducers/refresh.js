import { createSlice } from "@reduxjs/toolkit";
import * as Cud from "../thunks/cud";

const refreshReducer = createSlice({
    name: "refresh",
    initialState: { reloadCounter: 0, refreshErrorStatus: null },
    reducers: {},
    extraReducers: {
        [Cud.AddGroup.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.AddGroup.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.DelGroup.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.DelGroup.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.AddStudent.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.AddStudent.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.AddStudents.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.AddStudents.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.DelStudent.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.DelStudent.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.DelQuestions.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.DelQuestions.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.patchAnswer.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.patchAnswer.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.patchScore.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.patchScore.error]: (state, { status }) => { state.refreshErrorStatus = status },
        [Cud.patchEmail.fulfilled]: (state, _) => { state.reloadCounter++ },
        [Cud.patchEmail.error]: (state, { status }) => { state.refreshErrorStatus = status },
    }
});

export default refreshReducer.reducer