from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, response.json)

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 400)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'message': "A store with name 'test' already exists."}, response.json)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                response = client.delete('/store/test')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, response.json)
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('store/test')
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, response.json)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('store/test2')
                self.assertEqual(response.status_code, 404)
                self.assertIsNone(StoreModel.find_by_name('test2'))
                self.assertDictEqual({'message': 'Store not found'}, response.json)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/store/test')
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}, resp.json)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/stores')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': []}]}, resp.json)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/stores')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}]}, resp.json)
