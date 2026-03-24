from flask import Blueprint, jsonify, request
from services.request_service import RequestService

manager_bp = Blueprint('manager', __name__, url_prefix='/manager')


@manager_bp.get('/requests/<int:request_id>')
def get_request_card(request_id: int):
    item = RequestService.get_request_by_id(request_id)
    if not item:
        return jsonify({'error': 'Request not found'}), 404
    return jsonify(
        {
            'id': item.id,
            'subject': item.subject,
            'type': item.request_type,
            'priority': item.priority,
            'status': item.status,
            'description': item.description,
            'manager_comment': item.manager_comment,
            'reviewer_name': item.reviewer_name,
            'sla_hours': item.sla_hours,
            'overdue': item.is_overdue(),
        }
    )


@manager_bp.post('/requests/<int:request_id>/review')
def review_request(request_id: int):
    payload = request.get_json(force=True)
    item = RequestService.review_request(
        request_id=request_id,
        decision=payload['decision'],
        manager_name=payload['manager_name'],
        comment=payload.get('comment', ''),
    )
    return jsonify({'id': item.id, 'status': item.status, 'reviewer_name': item.reviewer_name})
