
#%%imports
import pytest
from lust_codesnippets_py.io import tables


#%%tests
class Test_generate_categorical_cmap:
    
    @pytest.fixture(
        params=[
            (
                [
                    {"name":"col1", "type":"str", "description": "column 1", "missing": None},
                    {"name":"col2", "type":"f32", "description": "column 2", "missing": None},
                ],
                "description", True, "//", None, '//{"description": ["description"], "$schema": [{"name": "col1", "type": "str", "description": "column 1", "missing": null}, {"name": "col2", "type": "f32", "description": "column 2", "missing": null}]}'
            ),
            (
                [
                    {"name":"col1", "type":"str", "description": "column 1", "missing": None},
                    {"name":"col2", "type":"f32", "description": "column 2", "missing": None},
                ],
                "description", False, "//", None, {'description': ['description'], '$schema': [{'name': 'col1', 'type': 'str', 'description': 'column 1', 'missing': None}, {'name': 'col2', 'type': 'f32', 'description': 'column 2', 'missing': None}]}
            ),
            (
                [
                    {"name":"col1", "type":"str", "description": "column 1", "missing": None},
                    {"name":"col2", "type":"f32", "description": "column 2", "missing": None},
                ],
                "description", True, "//", dict(indent=2), '//{\n//  "description": [\n//    "description"\n//  ],\n//  "$schema": [\n//    {\n//      "name": "col1",\n//      "type": "str",\n//      "description": "column 1",\n//      "missing": null\n//    },\n//    {\n//      "name": "col2",\n//      "type": "f32",\n//      "description": "column 2",\n//      "missing": null\n//    }\n//  ]\n//}',
            ),
        ]
    )
    def action(self, request):
        #arrange

        #act
        schema, description, as_string, comment_prefix, dumps_kwargs, header_true = request.param
        header = tables.make_header(schema=schema, description=description, as_string=as_string, comment_prefix=comment_prefix, dumps_kwargs=dumps_kwargs)
        return header, header_true

    #assert
    def test_intypes(self):
        schema = [{"name":"","type":"","description":"","missing":None}]
        with pytest.raises(AssertionError):        
            tables.make_header([{k:v for k, v in s.items() if k != "name"} for s in schema], "", )
            tables.make_header([{k:v for k, v in s.items() if k != "type"} for s in schema], "", )
            tables.make_header([{k:v for k, v in s.items() if k != "description"} for s in schema], "", )
            tables.make_header([{k:v for k, v in s.items() if k != "missing"} for s in schema], "", )

    def test_output(self, action):
        header, header_true = action
        assert header == header_true
    
    def test_outtypes(self, action):
        header, header_true = action
        assert isinstance(header, (dict, str))
