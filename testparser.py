import unittest
import jsonparser

test_string = r'''
{
    "null": null,
    "true": true,
    "false": false,
    "number": 163,
    "float": 1.63,
    "array": [
        1,
                             6,
        3
    ],
    "empty array": [],
    "empty string": "",
    "empty object": {},
    "object": {
        "space": " ",
        "backslash": "\\",
        "controls": "\b\f\n\r\t"
    },
    "one item array": [
        "a"
    ],
    "one item object": {
        "netease": "CC"
    }
}'''

test_string1 = r'''
{
    "null": null,
    "true": true,
    "false": false,
    "number": 163163163,
    "float": 1.63,
    "array": [
        1,
                             6,
        3
    ],
    "empty array": [],
    "empty string": "",
    "empty object": {},
    "object": {
        "space": " ",
        "backslash": "\\",
        "controls": "\b\f\n\r\t"
    },
    "one item array": [
        "a"
    ],
    "one item object": {
        "netease": "CC"
    }
}'''

test_dict = {
    "number": 163163163,
    "float": 1.63,
    "null": None,
    "true": True,
    "false": False,
    "array": [1, 6, 3],
    "empty array": [],
    "empty object": {}
}


class TestParser(unittest.TestCase):

    def test_string(self):
        parser1 = jsonparser.JsonParser()
        parser1.loads(test_string)
        parser2 = jsonparser.JsonParser()
        parser2.loads(parser1.dumps())
        self.assertEquals(parser1.dumps(), parser2.dumps())

    def test_file(self):
        parser1 = jsonparser.JsonParser()
        parser1.load_file("jsonFile.txt")
        parser1.dump_file("hahaha.txt")
        parser2 = jsonparser.JsonParser()
        parser2.load_file("hahaha.txt")
        self.assertEquals(parser1.dumps(), parser2.dumps())

    def test_dict(self):
        parser1 = jsonparser.JsonParser()
        parser1.load_dict(test_dict)
        parser2 = jsonparser.JsonParser()
        parser2.load_dict(parser1.dump_dict())
        self.assertEquals(parser1.dump_dict(), parser2.dump_dict())

    def test_update(self):
        parser1 = jsonparser.JsonParser()
        parser1.loads(test_string)
        parser2 = jsonparser.JsonParser()
        parser2.loads(test_string1)
        self.assertFalse(parser1.dumps() == parser2.dumps())
        parser1.update(test_dict)
        self.assertEquals(parser1.dumps(), parser2.dumps())

if __name__ == '__main__':
    unittest.main()
