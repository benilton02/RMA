from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Query

from src.main.composer.rma_create_composite import rma_create_composer
from src.main.composer.rma_update_composite import rma_update_composer
from src.main.composer.rma_get_composite import rma_get_composer
from src.main.composer.rma_common_defects_composite import rma_common_defect_composer
from src.main.composer.rma_step_average_composite import rma_step_average_composer

from src.main.schemas.rma.rma_input import RMAInput

from core.infra.redis.redis_cli import redis_dependency
from core.main.adapter.adapter import fastapi_adapter

from core.domain.security.jwt_auth import get_data
from core.utils.status_enum import RMAStatusEnum

rma_router = APIRouter()


rma_status_values = [
    RMAStatusEnum.PENDING,
    RMAStatusEnum.RECEIVED,
    RMAStatusEnum.FINISHED,
    RMAStatusEnum.TESTING,
    RMAStatusEnum.REFUND,
    RMAStatusEnum.REPAIR,
    RMAStatusEnum.REPLACEMENT,
]

@rma_router.post(
    '/rma',
    response_description='RMA',
    tags=['RMA'],
)
async def rma_create(
    rma_input: RMAInput,
    status: RMAStatusEnum = Query(rma_status_values),
    logged_user: str = Depends(get_data),
):
    """RMA create route"""
    request = {
        'query': {},
        'header': {},
        'body': {
            'rma': rma_input,
            'status': status,
            'logged_user': logged_user
            },
    }
    response = await fastapi_adapter(
        request=request, api_route=rma_create_composer()
    )

    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )


@rma_router.put(
    '/rma/{rma_id}',
    response_description='RMA',
    tags=['RMA'],
)
async def rma_update(
    rma_id: int,
    value: RMAStatusEnum = Query(rma_status_values),
    logged_user: str = Depends(get_data),
):
    """RMA Updated route"""
    request = {
        'query': {},
        'header': {},
        'body': {
            'rma_id': rma_id,
            'logged_user': logged_user,
            'value': value
            },
    }
    response = await fastapi_adapter(
        request=request, api_route=rma_update_composer()
    )

    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )
    

@rma_router.get(
    '/rma/defects',
    response_description='RMA',
    tags=['RMA'],
)
async def rma_commum_defects(
    logged_user: str = Depends(get_data),
):
    """RMA Updated route"""
    request = {
        'query': {},
        'header': {},
        'body': {'logged_user': logged_user},
    }
    response = await fastapi_adapter(
        request=request, api_route=rma_common_defect_composer()
    )

    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )
    

@rma_router.get(
    '/rma/average',
    response_description='RMA',
    tags=['RMA'],
)
async def rma_average_defects(
    logged_user: str = Depends(get_data),
):
    """RMA Updated route"""
    request = {
        'query': {},
        'header': {},
        'body': {
            'logged_user': logged_user
        },
    }
    response = await fastapi_adapter(
        request=request, api_route=rma_step_average_composer()
    )

    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )

@rma_router.get(
    '/rma/{rma_id}',
    response_description='RMA',
    tags=['RMA'],
)
async def rma_get_one(
    rma_id: int,
    logged_user: str = Depends(get_data),
):
    """RMA Updated route"""
    request = {
        'query': {},
        'header': {},
        'body': {"rma_id": rma_id},
    }
    response = await fastapi_adapter(
        request=request, api_route=rma_get_composer()
    )

    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )
    


