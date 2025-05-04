Table_Views = {'compitations': 'Компетенции', 
               'groups': 'Группы пользователей',
               'structure_compitations': 'Структуры компетенций',
               'tests': 'Тесты',
               'user_posts': 'Посты пользователей',
               'user_rights': 'Права пользователей',
               'users': 'Пользователи'}


def getView(keyView):
    if keyView in Table_Views:
        return Table_Views[keyView]
    else:  
        return keyView