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

my_dict = {
    "number": 163,
    "float": 1.63,
    "null": None,
    "true": True,
    "false": False,
    "array": [1, 6, 3],
    "empty array": [],
    "empty object": {}
}

import json
import jsonparser
def test_json():
    json_data = json.loads(test_string)
    print "json lib loads:"
    print(json_data)
    json_str = json.dumps(json_data)
    print "json lib dumps:"
    print(json_str)

my_dict["hahaha"] = 123456
print my_dict
'''
parser1 = jsonparser.JsonParser()
print "jsonparser1.loads"
parser1.loads(test_string)
print "jsonparser1.dumps:"
print parser1.dumps()

parser2 = jsonparser.JsonParser()
print "jsonparser2.load_file"
parser2.load_file("jsonFile.txt")
print "jsonparser2.dump:"
print parser2.dumps()
print "jsonparser2.dump_file"
parser2.dump_file("hahaha.txt")

parser3 = jsonparser.JsonParser()
print "jsonparser3.load_file"
parser3.load_file("hahaha.txt")
print "jsonparser3.dump:"
print parser3.dumps()

print "jsonparser3.load_dict"
parser3.load_dict(my_dict)
print "jsonparser3.dump:"
print parser3.dumps()
test_json()

test_dict = parser1.dump_dict()
print "test_dict:"
print test_dict
print "clear test_dict"
test_dict.clear()
print test_dict
print "jsonparser.dump:"
print parser1.dumps()
'''







