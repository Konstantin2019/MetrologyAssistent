import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { ReadExcel } from "../supportFunc";

const AddGroup = createAsyncThunk(
    'addGroupStatus',
    async (groupName, { rejectWithValue }) => {
        try {
            const url = '/api/admin/create_group';
            const token = sessionStorage.getItem('token');
            const response = await axios.get(url, { group_name: groupName }, { headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

const DelGroup = createAsyncThunk(
    'delGroupStatus',
    async (groupParams, { rejectWithValue }) => {
        try {
            const { groups, groupName } = groupParams;
            const group = groups.find(g => g.group_name === groupName);
            const url = `/api/admin/del_group/${group.id}`;
            const token = sessionStorage.getItem('token');
            const response = await axios.delete(url, { headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

const AddStudent = createAsyncThunk(
    'addStudentStatus',
    async (studentParams, { rejectWithValue }) => {
        try {
            const { surname, name, patronymic, email, selectedGroup } = studentParams;
            if (patronymic === (undefined || null)) {
                patronymic = ''
            }
            let student = {
                surname: surname.replace(/\s+/g, ''),
                name: name.replace(/\s+/g, ''),
                patronymic: patronymic.replace(/\s+/g, ''),
                email: email.replace(/\s+/g, '').toLowerCase(),
                group_id: selectedGroup.id
            };
            const url = '/api/admin/add_students';
            const token = sessionStorage.getItem('token');
            const response = axios.post(url, { students: student }, { headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

const AddStudents = createAsyncThunk(
    'addStudentsStatus',
    async (studentParams, { rejectWithValue }) => {
        try {
            const { e, groups } = studentParams;
            const records = await ReadExcel(e);
            const students = records.map(record => {
                const group_id = groups.find(g => g.group_name === record.Группа).map(g => g.id);
                if (!record.hasOwnProperty('Отчество')) {
                    record.Отчество = ''
                };
                const student = {
                    surname: record.Фамилия.replace(/\s+/g, ''),
                    name: record.Имя.replace(/\s+/g, ''),
                    patronymic: record.Отчество.replace(/\s+/g, ''),
                    email: record.Почта.replace(/\s+/g, '').toLowerCase(),
                    group_id: group_id
                };
                return student;
            }).filter(s => s.group_id !== (null || undefined));
            const url = '/api/admin/add_students';
            const token = sessionStorage.getItem('token');
            const response = await axios.post(url, { students: students }, { headers: { token: token } });
            return response.data;
        }
        catch (err) {
            let error = err;
            if (!error.response) { throw err }
            return rejectWithValue(error.response.status);
        };
    }
);

const DelStudent = createAsyncThunk(
    'delStudentStatus',
    async (studentId, { rejectWithValue }) => {
        try {
            const url = `/api/admin/del_student/${studentId}`;
            const token = sessionStorage.getItem('token');
            const response = await axios.delete(url, { headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

const DelQuestions = createAsyncThunk(
    'delQuestionsStatus',
    async (delParams, { rejectWithValue }) => {
        try {
            const { studentId, testName } = delParams;
            const url = '/api/admin/del_questions';
            const token = sessionStorage.getItem('token');
            const response = await axios.delete(url, { params: { student_id: studentId, test_name: testName }, headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

const patchAnswer = createAsyncThunk(
    'patchAnswerStatus',
    async (patchParams, { rejectWithValue }) => {
        try {
            const { questionId, answer, testName } = patchParams;
            const url = `/api/admin/patch_answer/${questionId}`;
            const token = sessionStorage.getItem('token');
            const response = await axios.post(url, { rk: testName, answer: answer }, { headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

const patchScore = createAsyncThunk(
    'patchScoreStatus',
    async (patchParams, { rejectWithValue }) => {
        try {
            const { questionId, score, testName } = patchParams;
            const url = `/api/admin/patch_score/${questionId}`;
            const token = sessionStorage.getItem('token');
            const response = await axios.post(url, { rk: testName, question_score: score }, { headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

const patchEmail = createAsyncThunk(
    'patchEmailStatus',
    async (patchParams, { rejectWithValue }) => {
        try {
            const { studentId, email } = patchParams;
            const url = `/api/admin/patch_email/${studentId}`;
            const token = sessionStorage.getItem('token');
            const response = await axios.post(url, { email: email }, { headers: { token: token } });
            return response.data;
        } catch (err) {
            let error = err;
            return rejectWithValue(error.response.status);
        }
    }
);

export { AddGroup, DelGroup, AddStudent, AddStudents, DelStudent, DelQuestions, patchAnswer, patchScore, patchEmail }