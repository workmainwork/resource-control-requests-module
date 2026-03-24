from app import create_app
from models import db, Request
from services.request_service import RequestService


def test_calculate_sla_hours_urgent():
    assert RequestService.calculate_sla_hours('urgent') == 8


def test_create_request_sets_sla_and_status():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')

    with app.app_context():
        db.drop_all()
        db.create_all()
        item = RequestService.create_request(
            subject='Тестовая заявка',
            request_type='purchase',
            priority='high',
            author_name='Тестовый пользователь',
            description='Описание',
        )
        assert item.status == 'new'
        assert item.sla_hours == 24


def test_review_request_changes_status():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')

    with app.app_context():
        db.drop_all()
        db.create_all()
        item = RequestService.create_request(
            subject='Тестовая заявка',
            request_type='it_support',
            priority='normal',
            author_name='Тестовый пользователь',
            description='Описание',
        )
        reviewed = RequestService.review_request(item.id, 'approve', 'Руководитель', 'Ок')
        assert reviewed.status == 'approved'
        assert reviewed.reviewer_name == 'Руководитель'
