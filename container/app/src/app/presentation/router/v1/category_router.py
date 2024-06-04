from fastapi import APIRouter, Request
from app.core.dependency import dependency_injector
from app.application.model import DefaultModel
from app.application.model.category_model import CategoryCreateModel, CategoryReadModel, CategoryUpdateModel
from app.presentation.controller.category_controller import CategoryController

router = APIRouter()

category_controller: CategoryController = dependency_injector.get(CategoryController)


@router.post("", response_model=DefaultModel)
def create_category(request: Request, data: CategoryCreateModel):
    return category_controller.create_category(request=request, data=data)


@router.get("", response_model=list[CategoryReadModel])
def get_all_category(request: Request):
    return category_controller.get_all_category(request=request)


@router.put("", response_model=DefaultModel)
def update_category(request: Request, data: CategoryUpdateModel):
    return category_controller.update_category(data=data)


@router.delete("/{id}", response_model=DefaultModel)
def delete_category(request: Request, id: int):
    return category_controller.update_category(id=id)
