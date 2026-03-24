def test_create_request_route(client):
    response = client.post('/employee/requests', json={
        'subject': 'Заявка на отпуск',
        'request_type': 'vacation',
        'priority': 'normal',
        'author_name': 'Иванов И.И.',
        'description': 'Отпуск на 14 дней',
        'estimated_cost': 0,
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'new'
    assert data['sla_hours'] == 48


def test_list_requests_route(client):
    client.post('/employee/requests', json={
        'subject': 'Заявка на закупку',
        'request_type': 'purchase',
        'priority': 'high',
        'author_name': 'Петров П.П.',
        'description': 'Закупить МФУ',
    })
    response = client.get('/employee/requests')
    assert response.status_code == 200
    assert len(response.get_json()) >= 1


def test_review_request_route(client):
    created = client.post('/employee/requests', json={
        'subject': 'Согласование документа',
        'request_type': 'approval',
        'priority': 'low',
        'author_name': 'Сидорова А.А.',
        'description': 'Согласовать регламент',
    })
    request_id = created.get_json()['id']

    response = client.post(f'/manager/requests/{request_id}/review', json={
        'decision': 'approve',
        'manager_name': 'Руководитель отдела',
        'comment': 'Согласовано',
    })
    assert response.status_code == 200
    assert response.get_json()['status'] == 'approved'
