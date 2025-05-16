Table_Views = {'compitations': {'name': 'Компетенции', 'columns': {'compitation_name': 'название компетенции', 'compitation_description': 'описание компетенции', 'complition_percent': 'процент для освоения'}}, 
               'groups': {'name': 'Группы пользователей', 'columns': {'group_name': 'название группы'}},
               'structure_compitations': {'name': 'Структуры компетенций', 'columns': {'struc_name': "название структуры", "struc_description": "описание структуры", "structure_file": "файл структуры", "creator_id": "id создателя"}},
               'tests': {'name': 'Тесты', 'columns': { 'test_name': 'название теста', 'test_description': "описание теста", 'test_length': "длительность теста", 'creation_date': "дата создания", 'last_update': "последние изменение", 'test_file': "файл теста", "creator_id": "id создателя" }},
               'user_posts': {'name': 'Посты пользователей', 'columns': {'post_name': 'заголовок', 'post_description': 'описание', 'post_datetime': 'дата публикации', "creator_id": "id создателя"}},
               'user_rights': {'name': 'Права пользователей', 'columns': {'description': 'описание права'}},
               'users': {'name': 'Пользователи', 'columns': {'username': 'логин', "password": "пароль", "third_Name": "отчество", "second_Name": "фамилия", "first_Name": "имя"}}}




def getView(keyView):
    if keyView in Table_Views:
        return Table_Views[keyView]['name']
    else:  
        return keyView