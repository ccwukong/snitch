from enum import Enum


class TaskType(Enum):
    HEALTH_CHECK = 'hc'
    IDEMPOTENCY_CHECK = 'id'
