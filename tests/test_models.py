from src.models import Task
import datetime
import pytest


class TestTaskModels:
    def test_create_task_model(self):
        task = Task(id=1, title="Test", description="Test desc", due_date="2024-12-31")
        assert task.id == 1
        assert task.title == "Test"
        assert task.description == "Test desc"
        assert task.due_date == datetime.date(2024, 12, 31)

    def test_create_task_model_invalid_date(self):
        with pytest.raises(ValueError):
            Task(id=2, title="Test 2", description="Test desc 2", due_date="31-12-2024")

    def test_create_task_model_no_due_date(self):
        task = Task(id=3, title="Test 3", description=None)
        assert task.id == 3
        assert task.title == "Test 3"
        assert task.description is None
        assert task.due_date is None

    def test_create_task_model_no_description(self):
        task = Task(id=4, title="Test 4", due_date="2024-11-30")
        assert task.id == 4
        assert task.title == "Test 4"
        assert task.description is None
        assert task.due_date == datetime.date(2024, 11, 30)

    def test_create_task_model_minimal(self):
        task = Task(id=5, title="Test 5")
        assert task.id == 5
        assert task.title == "Test 5"
        assert task.description is None
        assert task.due_date is None

    def test_create_task_model_invalid_id(self):
        with pytest.raises(ValueError):
            Task(
                id="invalid",
                title="Test 6",
                description="Test desc 6",
                due_date="2024-10-10",
            )

    def test_create_task_model_empty_title(self):
        with pytest.raises(ValueError):
            Task(id=7, title=None, description="Test desc 7", due_date="2024-09-09")

    # def test_create_task_model_whitespace_title(self):
    #     with pytest.raises(ValueError):
    #         Task(id=8, title="   ", description="Test desc 8", due_date="2024-08-08")

    def test_create_task_model_invalid_due_date_type(self):

        with pytest.raises(ValueError):
            Task(id=9, title="Test 9", description="Test desc 9", due_date=20240610)

    def test_create_task_model_invalid_due_date_format(self):
        with pytest.raises(ValueError):
            Task(
                id=10,
                title="Test 10",
                description="Test desc 10",
                due_date="2024/06/10",
            )
