from fastapi import APIRouter, Request
from app.core.dependency import dependency_injector
from app.application.model.priority_model import PriorityReadModel
from app.presentation.controller.priority_controller import PriorityController

router = APIRouter()

priority_controller: PriorityController = dependency_injector.get(PriorityController)


@router.get("", response_model=list[PriorityReadModel])
def get_all_priority(request: Request):
    return priority_controller.get_all_priority()
