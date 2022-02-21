'''
Data type for optional username or password
'''
from behave import register_type, use_step_matcher
import parse
@parse.with_pattern(r".*")
def parse_string(text):
    output = text.strip()
    if output == 'NULL':
        output = None
    return output
def init_opt_():
    '''
    Registers the opt_ type and activates the cfparse step matcher. Once this is done, you should be able to make step parameters optional.
    
    For example, if you have a parameter {username}, replace it with {username:opt_?}
    '''
    register_type(opt_=parse_string)
    use_step_matcher("cfparse")