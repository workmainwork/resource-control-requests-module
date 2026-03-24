from app import create_app
from models import db, Request
from services.request_service import RequestService

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    demo_items = [
        {
            'subject': 'Заявка на закупку ноутбука',
            'request_type': 'purchase',
            'priority': 'high',
            'author_name': 'Иванов И.И.',
            'description': 'Необходимо закупить ноутбук для нового сотрудника',
            'estimated_cost': 90000,
        },
        {
            'subject': 'Согласование командировки',
            'request_type': 'business_trip',
            'priority': 'normal',
            'author_name': 'Петров П.П.',
            'description': 'Командировка в филиал на 3 дня',
            'estimated_cost': 25000,
        },
        {
            'subject': 'Обращение в ИТ-поддержку',
            'request_type': 'it_support',
            'priority': 'urgent',
            'author_name': 'Сидорова А.А.',
            'description': 'Не работает корпоративная почта',
            'estimated_cost': 0,
        },
    ]

    for item in demo_items:
        RequestService.create_request(**item)

    print('Demo data loaded successfully.')
