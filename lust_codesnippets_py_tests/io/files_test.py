
#%%imports
import pytest
from lust_codesnippets_py.io import files


#%%tests
class Test_generate_categorical_cmap:
    
    @pytest.fixture(
        params=[
            (
                "./temp.txt", "prefix to file\n", 'prefix to file\nexemplary main body content',
            ),
        ]
    )
    def action(self, request):
        #arrange

        #act
        filename, s, f_true_content = request.param
        ##create a file
        with open(filename, "w") as f:
            f.write("exemplary main body content")
        
        files.prepend(filename=filename, s=s)
        return filename, f_true_content

    #assert
    def test_filecontent(self, action):
        filename, f_true_content = action
        with open(filename, "r") as f:
            content = f.read()
        assert content == f_true_content
