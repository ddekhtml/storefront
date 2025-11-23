from rest_framework import status
from django.contrib.auth.models import User
import pytest
from model_bakery import baker
from store.models import Collection, Product

@pytest.fixture
def creare_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collection/', collection)
    return do_create_collection 

@pytest.mark.django_db
class TestCreateCollection:
    
    def test_if_user_is_anonymus_returns_401(self, creare_collection):
        #AAA(Arrange (system/object/database), Act(behaviour), Assert (expect))

        response = creare_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    def test_if_user_is_not_admin_returns_403(self,authenticate,creare_collection):
        #AAA(Arrange (system/object/database), Act(behaviour), Assert (expect))

        authenticate()
        response = creare_collection({'title': 'a'})
 
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_data_is_invalid_returns_400(self, authenticate, creare_collection):
        #AAA(Arrange (system/object/database), Act(behaviour), Assert (expect))

        authenticate(is_staff=True)
        response = creare_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None 

    def test_if_data_is_valid_returns_201(self, authenticate, creare_collection):
        #AAA(Arrange (system/object/database), Act(behaviour), Assert (expect))

        authenticate(is_staff=True)
        response = creare_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id']>0

        
@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        # Arrange 
        collection= baker.make(Collection)
        response=api_client.get(f"/store/collection/{collection.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == collection.id 
        assert response.data['title'] ==collection.title
