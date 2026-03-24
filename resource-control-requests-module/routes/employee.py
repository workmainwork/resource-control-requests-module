from flask import Blueprint, jsonify, request
from services.request_service import RequestService

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.get('/requests')
def list_requests():
    status = request.args.get('status', 'all')
    items = RequestService.get_requests(status=status)
    return jsonify([
        {
            'id': item.id,
            'subject': item.subject,
            'type': item.request_type,
            'priority': item.priority,
            'status': item.status,
            'sla_hours': item.sla_hours,
        }
        for item in items
    ])


@employee_bp.post('/requests')
def create_request():
    payload = request.get_json(force=True)
    item = RequestService.create_request(
        subject=payload['subject'],
        request_type=payload['request_type'],
        priority=payload.get('priority', 'normal'),
        author_name=payload['author_name'],
        description=payload.get('description', ''),
        estimated_cost=payload.get('estimated_cost', 0.0),
    )
    return jsonify({'id': item.id, 'status': item.status, 'sla_hours': item.sla_hours}), 201
