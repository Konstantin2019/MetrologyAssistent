import * as XLSX from 'xlsx';
import * as FileSaver from 'file-saver';

const ReadExcel = (e) => {
    let excelFile = e.target.files[0];
    let promise = new Promise((resolve, reject) => {
        let fileReader = new FileReader();
        fileReader.readAsArrayBuffer(excelFile);
        fileReader.onload = (e) => {
            let buffer = e.target.result;
            let workbook = XLSX.read(buffer, { type: 'buffer' });
            let sheetName = workbook.SheetNames[0];
            let sheet = workbook.Sheets[sheetName];
            let data = XLSX.utils.sheet_to_json(sheet);
            resolve(data);
        };
        fileReader.onerror = (e) => reject(e);
    });
    e.target.value = null;
    return promise;
};

const LoadToExcel = (students, fileName) => {
    let studentsToLoad = students.map(student => {
        let studentToLoad = {
            Фамилия: student.surname,
            Имя: student.name,
            Отчество: student.patronymic,
            РК1: student.rk1_score,
            РК2: student.rk2_score,
            Зачёт: student.test_score
        };
        return studentToLoad;
    });
    let fileType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
    let fileExtension = '.xlsx';
    let worksheet = XLSX.utils.json_to_sheet(studentsToLoad);
    let workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, fileName);
    let excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    let result = new Blob([excelBuffer], { type: fileType });
    FileSaver.saveAs(result, fileName + fileExtension);
};

export { ReadExcel, LoadToExcel }