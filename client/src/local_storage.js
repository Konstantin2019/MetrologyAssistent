export default function GetData() {
    const tests = [
        {
            id: 1,
            test_name: 'rk1',
            test_view: 'РК№1'
        },
        {
            id: 2,
            test_name: 'rk2',
            test_view: 'РК№2'
        },
        {
            id: 3,
            test_name: 'test',
            test_view: 'Зачёт'
        }
    ];
    const teachers = [
        {
            id: 1,
            teacher_name: 'potapov',
            teacher_view: 'Потапов К.Г.'
        },
        {
            id: 2,
            teacher_name: 'tumakova',
            teacher_view: 'Тумакова Е.В.'
        }
    ];
    return { tests, teachers }
}