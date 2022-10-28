import { createAsyncThunk } from "@reduxjs/toolkit";

const fetchAll = createAsyncThunk(
    'fetchAllStatus',
    async (url, { rejectWithValue }) => {
        try {
            const response = await axios.get(url);
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.message);
        }
    }
);

export { fetchAll };
