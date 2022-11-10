def select(name):
    if name == 'potapov':
        from api.core.teachers.potapov import checker, task1_loader, task2_loader, test_loader
        return checker, task1_loader, task2_loader, test_loader
    elif name == 'tumakova':
        from api.core.teachers.tumakova import checker, task1_loader, task2_loader, test_loader
        return checker, task1_loader, task2_loader, test_loader