# import unittest
# from core.rest_response import RestResponse
# 
# class TestRestResponse(unittest.TestCase):
#     def test_should_map_all_properties(self):
#         """
#         Assert that all properties are mapped correctly to properties on the
#         object.
#         """
#         # Arrange, Act
#         response = RestResponse(
#             200,
#             'TestMessage',
#             'TestDetail',
#             {'test': 'abc'},
#             True)
# 
#         # Assert
#         self.assertEqual(response.code, 200)
#         self.assertEqual(response.message, 'TestMessage')
#         self.assertEqual(response.detail, 'TestDetail')
#         self.assertEqual(response.data, {'test': 'abc'})
#         self.assertEqual(response.is_success, True)
# 
#     def test_should_map_to_dictionary_via_json_with_status(self):
#         """
#         Assert that when a status code is passed in, the json() output returns
#         a tuple including the status code.
#         """
#         # Arrange
#         response = RestResponse(
#             201,
#             'TestMessage',
#             'TestDetail',
#             {'test': 'abc'},
#             False
#         )
# 
#         # Act
#         json_response = response.json()
#         data = json_response[0]
#         response_code = json_response[1]
# 
#         # Assert
#         self.assertEqual(response_code, 201)
#         self.assertEqual(data['code'], 201)
#         self.assertEqual(data['message'], 'TestMessage')
#         self.assertEqual(data['detail'], 'TestDetail')
#         self.assertEqual(data['data'], {'test': 'abc'})
#         self.assertEqual(data['isSuccess'], False)
# 
#     def test_should_map_to_dictionary_via_json_without_status(self):
#         """
#         Check that without a status code, the json function doesn't return
#         a tuple including the status code.
#         """
#         # Arrange
#         response = RestResponse(
#             None,
#             'TestMessage',
#             'TestDetail',
#             {'test': 'abc'},
#             False
#         )
# 
#         json_response = response.json()
# 
#         # Assert
#         self.assertRaises(KeyError, lambda: json_response['code'])
# 
#     def test_should_map_to_dictionary_via_json_without_properties(self):
#         """
#         Assert that when each parameter is passed None, it does not appear
#         in the json() output.
#         """
#         # Arrange
#         response = RestResponse(
#             None,
#             None,
#             None,
#             None,
#             None
#         )
# 
#         # Act
#         json_response = response.json()
# 
#         # Assert
#         self.assertRaises(KeyError, lambda: json_response['message'])
#         self.assertRaises(KeyError, lambda: json_response['detail'])
#         self.assertRaises(KeyError, lambda: json_response['data'])
#         self.assertRaises(KeyError, lambda: json_response['isSuccess'])
# 