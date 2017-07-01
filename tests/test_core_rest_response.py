import unittest
from core.rest_response import RestResponse

class TestRestResponse(unittest.TestCase):
    def test_should_map_all_properties(self):
        # Arrange, Act
        response = RestResponse(
            200,
            'TestMessage',
            'TestDetail',
            {'test': 'abc'},
            True)

        # Assert
        self.assertEqual(response.code, 200)
        self.assertEqual(response.message, 'TestMessage')
        self.assertEqual(response.detail, 'TestDetail')
        self.assertEqual(response.data, {'test': 'abc'})
        self.assertEqual(response.is_success, True)

    def test_should_map_to_dictionary_via_json_with_status(self):
        # Arrange
        response = RestResponse(
            201,
            'TestMessage',
            'TestDetail',
            {'test': 'abc'},
            False
        )

        json_response = response.json()
        data = json_response[0]
        response_code = json_response[1]

        # Assert
        self.assertEqual(response_code, 201)
        self.assertEqual(data['code'], 201)
        self.assertEqual(data['message'], 'TestMessage')
        self.assertEqual(data['detail'], 'TestDetail')
        self.assertEqual(data['data'], {'test': 'abc'})
        self.assertEqual(data['isSuccess'], False)

    def test_should_map_to_dictionary_via_json_without_status(self):
        # Arrange
        response = RestResponse(
            None,
            'TestMessage',
            'TestDetail',
            {'test': 'abc'},
            False
        )

        json_response = response.json()

        # Assert
        self.assertRaises(KeyError, lambda: json_response['code'])

    def test_should_map_to_dictionary_via_json_without_properties(self):
        # Arrange
        response = RestResponse(
            None,
            None,
            None,
            None,
            None
        )

        # Act
        json_response = response.json()

        # Assert
        self.assertRaises(KeyError, lambda: json_response['message'])
        self.assertRaises(KeyError, lambda: json_response['detail'])
        self.assertRaises(KeyError, lambda: json_response['data'])
        self.assertRaises(KeyError, lambda: json_response['isSuccess'])
