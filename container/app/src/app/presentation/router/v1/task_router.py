from fastapi import APIRouter, Request
from app.core.dependency import dependency_injector
from app.application.model import DefaultModel
from app.application.model.task_model import TaskCreateModel, TaskReadModel, TaskUpdateModel
from app.presentation.controller.task_controller import TaskController

router = APIRouter()

task_controller: TaskController = dependency_injector.get(TaskController)


@router.post("", response_model=DefaultModel)
def create_task(request: Request, data: TaskCreateModel):
    return task_controller.create_task(request=request, data=data)


@router.get("", response_model=list[TaskReadModel])
def get_all_task(request: Request):
    return task_controller.get_all(request=request)


@router.put("", response_model=DefaultModel)
def update_task(request: Request, data: TaskUpdateModel):
    return task_controller.update_task(data=data)


@router.delete("/{id}", response_model=DefaultModel)
def delete_task(request: Request, id: int):
    return task_controller.done_task(id=id)


@router.get("/done/{id}", response_model=DefaultModel)
def done_task(request: Request, id: int):
    return task_controller.done_task(id=id)
