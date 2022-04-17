def select(name):
    if name == 'potapov':
        from api.modules.teachers.potapov import checker, task1_loader, task2_loader
        return checker, task1_loader, task2_loader
    elif name == 'tumakova':
        from api.modules.teachers.tumakova import checker, task1_loader, task2_loader
        return checker, task1_loader, task2_loader