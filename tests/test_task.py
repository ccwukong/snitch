from snitch.task_runners.task import TaskType, Task, TaskQueue
import unittest


class TestTaskType(unittest.IsolatedAsyncioTestCase):
    def test_TaskType(self):
        self.assertEqual(TaskType.HEALTH_CHECK.value, 'hc')
        self.assertEqual(TaskType.IDEMPOTENCY_CHECK.value, 'id')

    async def test_TaskQueue(self):
        async def dummy_func(a):
            return a

        task_queue = TaskQueue()
        task_queue.add_task(Task(dummy_func, 1))
        self.assertEqual(len(task_queue), 1)

        task = task_queue.pop_task()

        self.assertEqual(await task.task(task.args), 1)
