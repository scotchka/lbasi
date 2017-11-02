from src.list_parser import Parse

parse = Parse()


def test():
    assert [19, 22, 23] == parse('  [ 19 , 22 , 23    ]    ')
    assert [[1], 3, [[2]]] == parse('[[1],  3, [ [2] ]]')
    assert [[42]] == parse('[ [ 42 ] ]')
    assert [[[]], []] == parse('[ [ [ ] ] , [ ]   ]')
    assert False is parse('[ 1 ] ] ')
    assert False is parse(' [ [ 1 ]   ')
    assert False is parse('[1 3]')
    assert False is parse('12, 45')
    assert False is parse('[12')
