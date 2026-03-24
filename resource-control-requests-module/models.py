from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='normal')
    status = db.Column(db.String(20), nullable=False, default='new')
    desired_due_date = db.Column(db.DateTime, nullable=True)
    estimated_cost = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=False, default='')
    manager_comment = db.Column(db.Text, nullable=False, default='')
    author_name = db.Column(db.String(120), nullable=False)
    reviewer_name = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sla_hours = db.Column(db.Integer, nullable=False, default=24)

    def is_overdue(self) -> bool:
        if self.status in ('approved', 'rejected', 'done'):
            return False
        return datetime.utcnow() > self.created_at + timedelta(hours=self.sla_hours)
