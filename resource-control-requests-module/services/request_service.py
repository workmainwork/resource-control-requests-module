from __future__ import annotations

from models import db, Request


class RequestService:
    """Сервисный слой для создания и рассмотрения заявок."""

    SLA_BY_PRIORITY = {
        'low': 72,
        'normal': 48,
        'high': 24,
        'urgent': 8,
    }

    @classmethod
    def calculate_sla_hours(cls, priority: str) -> int:
        return cls.SLA_BY_PRIORITY.get(priority, 48)

    @classmethod
    def create_request(
        cls,
        subject: str,
        request_type: str,
        priority: str,
        author_name: str,
        description: str,
        desired_due_date=None,
        estimated_cost: float = 0.0,
    ) -> Request:
        request_obj = Request(
            subject=subject,
            request_type=request_type,
            priority=priority,
            status='new',
            desired_due_date=desired_due_date,
            estimated_cost=estimated_cost,
            description=description,
            author_name=author_name,
            sla_hours=cls.calculate_sla_hours(priority),
        )
        db.session.add(request_obj)
        db.session.commit()
        return request_obj

    @staticmethod
    def get_requests(status: str | None = None) -> list[Request]:
        query = Request.query.order_by(Request.created_at.desc())
        if status and status != 'all':
            query = query.filter_by(status=status)
        return query.all()

    @staticmethod
    def get_request_by_id(request_id: int) -> Request | None:
        return Request.query.get(request_id)

    @staticmethod
    def review_request(request_id: int, decision: str, manager_name: str, comment: str = '') -> Request:
        request_obj = Request.query.get_or_404(request_id)
        mapping = {
            'approve': 'approved',
            'reject': 'rejected',
            'take': 'in_progress',
        }
        request_obj.status = mapping.get(decision, request_obj.status)
        request_obj.reviewer_name = manager_name
        request_obj.manager_comment = comment
        db.session.commit()
        return request_obj
