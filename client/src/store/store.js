import { configureStore } from "@reduxjs/toolkit";
import yearReducer from "./reducers/year";
import groupReducer from "./reducers/group";
import studentReducer from "./reducers/student";
import refreshReducer from "./reducers/refresh";

const store = configureStore({ 
    reducer: {
        years: yearReducer,
        groups: groupReducer,
        students: studentReducer,
        refresh: refreshReducer
    }
});

export { store }