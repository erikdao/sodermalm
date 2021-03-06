from datetime import datetime

from sqlalchemy import Column, DateTime, event


class TimeStampMixin(object):
    """Timestampin mixin, i.e., automatically add `created_at`
    and `updated_at` columns to your model"""
    created_at = Column(DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_update', cls._updated_at)
