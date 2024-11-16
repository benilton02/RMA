import sys
import os


# Add the parent directory of 'app' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from unittest.mock import MagicMock
from core.infra.db.repositories.rma_repository import RMARespository
from core.infra.db.repositories.user_repository import UserRepository
from core.infra.db.entities.rma_entity import RMA
from src.data.rma.rma_use_cases import RMAUseCases


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository)

@pytest.fixture
def mock_rma_repository():
    return MagicMock(spec=RMARespository)

@pytest.fixture
def rma_use_case(mock_rma_repository, mock_user_repository):
    return RMAUseCases(
        rma_repository=mock_rma_repository,
        user_repository=mock_user_repository
    )

def test_create_rma_success(rma_use_case, mock_user_repository, mock_rma_repository):
    user_mock = MagicMock()
    user_mock.id = 1
    mock_user_repository.find_user_by_email.return_value = user_mock
    
    rma_mock = MagicMock()
    rma_mock.name = 'Phone'
    rma_mock.description = 'Screen cracked'
    rma_mock.defect = 'Crack'
    rma_mock.model = 'XYZ123'
    rma_mock.color = 'Black'
    rma_mock.serial_number = 'serial_number'

    data = {
        'logged_user': {'email': 'testuser@example.com'},
        'rma': rma_mock,
        'status': 'Pending'
    }

    mock_rma_repository.create_rma.return_value = 1234 

    result = rma_use_case.create(data)

    assert result['success'] is True
    assert result['code'] == 200
    assert result['data']['message'] == 'RAM created successfully'
    assert result['data']['rma_id'] == 1234
    
    mock_user_repository.find_user_by_email.assert_called_once_with('testuser@example.com')
    mock_rma_repository.create_rma.assert_called_once()
    

def test_update_rma_success(rma_use_case, mock_user_repository, mock_rma_repository):
    user_mock = MagicMock()
    user_mock.id = 1
    mock_user_repository.find_user_by_email.return_value = user_mock
    
    rma_mock = MagicMock(spec=RMA)
    rma_mock.id = 1234
    rma_mock.status = []
    mock_rma_repository.get_rma_by_id.return_value = rma_mock
    
    data = {
        'logged_user': {'email': 'testuser@example.com'},
        'rma_id': 1234,
        'value': 'Updated'
    }
    
    mock_rma_repository.update_rma.return_value = True

    result = rma_use_case.update(data)

    assert result['success'] is True
    assert result['code'] == 200
    assert result['data']['message'] == 'The RMA was updated successfully'
    
    
    mock_user_repository.find_user_by_email.assert_called_once_with('testuser@example.com')
    mock_rma_repository.get_rma_by_id.assert_called_once_with(1234)
    mock_rma_repository.update_rma.assert_called_once_with(rma_mock)
    
    assert len(rma_mock.status) == 1
    assert rma_mock.status[0].status == 'Updated'
    assert rma_mock.status[0].user_id == user_mock.id
    

def test_get_rma_success(rma_use_case, mock_rma_repository):
    rma_mock = MagicMock(spec=RMA)
    rma_mock.id = 1234
    rma_mock.product_name = "Product Example"
    rma_mock.defect_description = "Defect example"
    
    data = {
        'rma_id': 1234
    }
    
    mock_rma_repository.get_rma_by_id.return_value = rma_mock

    result = rma_use_case.get_rma(data)

    assert result['success'] is True
    assert result['code'] == 200
    assert result['data']['rma'] == rma_mock
    assert result['data']['rma'].id == 1234
    assert result['data']['rma'].product_name == "Product Example"
    assert result['data']['rma'].defect_description == "Defect example"
    
    mock_rma_repository.get_rma_by_id.assert_called_once_with(1234)
    

def test_get_common_defect_success(rma_use_case, mock_rma_repository):
    result_mock = [
        ('Defect A', 100),
        ('Defect B', 50)
    ]
    
    mock_rma_repository.get_common_defect.return_value = result_mock
    
    logged_user_mock = {'logged_user': {'id': 1, 'user_name': 'admin user', 'email': 'admin@email.com', 'roles': [{'id': 1, 'value': 'ADMIN', 'label': 'Admin', 'description': 'Major permission.'}], 'exp': 1731645126}}
    
    result = rma_use_case.get_common_defect(logged_user_mock)

    assert result['success'] is True
    assert result['code'] == 200
    assert 'items' in result['data']
    assert len(result['data']['items']) == 2
    assert result['data']['items'][0]['defect'] == 'Defect A'
    assert result['data']['items'][0]['total'] == 100
    assert result['data']['items'][1]['defect'] == 'Defect B'
    assert result['data']['items'][1]['total'] == 50
    
    mock_rma_repository.get_common_defect.assert_called_once()


def test_step_average_success(rma_use_case, mock_rma_repository):
    result_mock = [
        ('Pending', 3600),  
        ('Completed', 7200)
    ]
    
    mock_rma_repository.step_average.return_value = result_mock
    
    logged_user_mock = logged_user_mock = {'logged_user': {'id': 1, 'user_name': 'admin user', 'email': 'admin@email.com', 'roles': [{'id': 1, 'value': 'ADMIN', 'label': 'Admin', 'description': 'Major permission.'}], 'exp': 1731645126}}
    
    result = rma_use_case.step_average(logged_user_mock)

    assert result['success'] is True
    assert result['code'] == 200
    assert 'items' in result['data']
    assert len(result['data']['items']) == 2
    assert result['data']['items'][0]['status'] == 'Pending'
    assert result['data']['items'][0]['avg_duration_hours'] == 1.0
    assert result['data']['items'][1]['status'] == 'Completed'
    assert result['data']['items'][1]['avg_duration_hours'] == 2.0
    
    mock_rma_repository.step_average.assert_called_once()