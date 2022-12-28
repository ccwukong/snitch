from src.snitch.task_runners.task import TaskType
import unittest


class TestTaskType(unittest.TestCase):
    def test_TaskType(self):
        self.assertEqual(TaskType.HEALTH_CHECK.value, 'hc')
        self.assertEqual(TaskType.IDEMPOTENCY_CHECK.value, 'id')
