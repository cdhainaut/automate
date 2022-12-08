import json as _ojson

'''
Overwrite load and loads function from json.

'''
def load(file_input:str,**kwargs) -> dict :
    with open(file_input,'r') as fp:
        return loads(fp.read(),**kwargs)
def loads(s,to_parse:dict=None,splitter="@") -> dict:
    '''
    Just adds two arguments to the base function:
    - to_parse: Dictionary needed to parse values in the json file
    - splitter: string which is used for targetting the values to change in the template
    '''
    if to_parse is not None:
        for column,value in to_parse.items():
            s = s.replace(f'{splitter}{column}{splitter}',str(*value))
    return _ojson.loads(s)

