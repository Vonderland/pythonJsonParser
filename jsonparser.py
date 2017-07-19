#coding=UTF-8
import string

space_chars = [' ', '\n', '\t']
escape_char = '\\'
escape_chars = {'\"': '"', '\\': '\\', '\b': 'b', '\f': 'f', '\n': 'n', '\r': 'r', '\t': 't'}


def skip_space(s, index):
    '''跳过字符串中多余的空格,制表符和回车'''
    while s[index] in space_chars:
        index += 1
    return index


def make_escape(c):
    if c == '"':
        return '"'
    if c == '\\':
        return '\\'
    if c == '/':
        return '/'
    if c == 'b':
        return '\b'
    if c == 'f':
        return '\f'
    if c == 'n':
        return '\n'
    if c == 't':
        return '\t'
    if c == 'r':
        return '\r'
    raise ValueError("Invalid escape char")


def make_string(s):
    index = 0
    index = skip_space(s, index)
    if s[index] != '"':
        raise ValueError("Invalid Json object, not a string")
    index += 1
    result = unicode("")
    while index < len(s):
        c = s[index]
        index += 1
        if c == escape_char:
            c = s[index]
            index += 1
            result += make_escape(c)
        elif c == '"':
            break
        else:
            result += c
    return result, index


def make_array(s):
    index = 0
    index = skip_space(s, index)
    if s[index] != '[':
        raise ValueError("Invalid Json object, not an array, no '['")
    index += 1
    index = skip_space(s, index)
    array = []
    if s[index] == ']':
        return array, index + 1
    while True:
        value, offset = make_value(s[index:])
        array.append(value)
        index += offset
        index = skip_space(s, index)
        if s[index] != ',':  # 不是逗号，可能是读到数组尾或者是异常
            break
        index += 1  # 跳过逗号
        # index = skip_space(s, index)
    if s[index] != ']':
        raise ValueError("Invalid Json object, not an array, no ']'")
    return array, index + 1


def make_value(s):
    index = 0
    index = skip_space(s, index)
    if s[index] == '[':  # 数组
        result, offset = make_array(s[index:])
    elif s[index] == '{':  # 对象
        result, offset = make_object(s[index:])
    elif s[index] == '"':  # string
        result, offset = make_string(s[index:])
    elif s.find("true", index, index + 4) != -1:  # bool, True
        result = True
        offset = 4
    elif s.find("false", index, index + 5) != -1:  # bool, False
        result = False
        offset = 5
    elif s.find("null", index, index + 4) != -1:  # None
        result = None
        offset = 4
    else:
        result, offset = make_number(s[index:])  # 余下的情况当作数字来处理
    return result, index + offset


def make_number(s):
    index = 0
    end = 0
    while s[end] not in {' ', '\n', '\t', ']', '}', ','}:
        end += 1
    if index == end:
        raise ValueError("Invalid number")  #空数字
    number = s[index:end]
    if '.' in number or 'e' in number or 'E' in number:
        num = float(number)
    else:
        num = int(number)
    return num, end
    

def make_object(s):
    '''由String生成对应字典'''
    dic = {}
    index = skip_space(s, 0);
    if s[index] != '{':
        raise ValueError("Invalid Json object, lack of '{'")
    index += 1
    index = skip_space(s, index);
    if s[index] == '}':
        return dic, index + 1
    while True:
        key, offset = make_string(s[index:])
        index += offset
        index = skip_space(s, index)
        if s[index] != ':':
            raise ValueError("Invalid Json object, lack of ':'")
        index += 1
        value, offset = make_value(s[index:])
        index += offset
        dic[key] = value
        index = skip_space(s, index)
        if s[index] != ',':  # 不是逗号，可能是读到对象尾或者异常
            break
        index += 1
    if s[index] != '}':
        raise ValueError("Invalid Json object, lack of '}'")
    return dic, index + 1


def make_json_string(s):
    result = '"'
    for c in s:
        if c in escape_chars.keys():
            result = result + "\\" + escape_chars[c]
        else:
            result += c
    result += '"'
    return result


def make_json_array(array):
    result = '['
    for i in array:
        result = result + make_json_value(i) + ','
    if len(array) > 0:
        result = result[:-1]  # 去掉最后一个逗号
    result += ']'
    return result


def make_json_value(value):
    if isinstance(value, bool):
        if value:
            return "true"
        else:
            return "false"
    if value is None:
        return "null"
    if isinstance(value, dict):
        return dict2json(value)
    if isinstance(value, list):
        return make_json_array(value)
    if isinstance(value, unicode):
        return make_json_string(value)
    if isinstance(value, int) or isinstance(value, float):
        return unicode(value)
    print "make_json_value(value): Fail to make Json value" + value


def dict2json(dic):
    result = "{"
    for i in dic.keys():
        result = result + make_json_string(i) + ":" + make_json_value(dic[i]) + ","
    if len(dic) > 0:
        result = result[:-1]  # 去掉最后一个逗号
    result += "}"
    return result


def deep_copy(value):
    if isinstance(value, list):
        copy_list = []
        for each in value:
            copy_list.append(deep_copy(each))
        return copy_list
    if isinstance(value, dict):
        copy_dict = {}
        for key in value.keys():
            copy_dict[key] = deep_copy(value[key])
        return copy_dict
    return value


class JsonParser:
    def __init__(self):
        self._data = {}
        self._index = 0

    def loads(self, s):
        self._data, self._index = make_object(s)

    def dumps(self):
        return dict2json(self._data)

    def load_file(self, f):
        try:
            with open(f, "r") as json_file:
                s = json_file.read()
        except IOError:
            raise IOError("Fail to read file")
        finally:
            json_file.close()
        self._data, self._index = make_object(s)

    def dump_file(self, f):
        try:
            with open(f, "w") as json_file:
                s = JsonParser.dumps(self)
                json_file.write(s)
        except IOError:
            raise IOError("Fail to write file")
        finally:
            json_file.close()

    def load_dict(self, d):
        self._data = {}
        for key in d.keys():
            if isinstance(key, str) or isinstance(key, unicode):  # key不是字符串时忽略
                self._data[key] = deep_copy(d[key])

    def dump_dict(self):
        return deep_copy(self._data)

    def update(self, d):
        for key in d.keys():
            if isinstance(key, str) or isinstance(key, unicode):  # key不是字符串时忽略
                self._data[key] = deep_copy(d[key])

    def __getitem__(self, key):
        return deep_copy(self._data[key])

    def __setitem__(self, key, value):
        if isinstance(key, str) or isinstance(key, unicode):  # key不是字符串时忽略
                self._data[key] = deep_copy(value)
