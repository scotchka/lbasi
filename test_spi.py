import pytest
from spi import Lexer, Parser, Interpreter, SemanticAnalyzer
from src.symbol import BuiltinTypeSymbol, VarSymbol
from src.errors import UndeclaredVariable, DuplicateDeclaration

integer_type = BuiltinTypeSymbol('INTEGER')
real_type = BuiltinTypeSymbol('REAL')


def test_interpreter():
    text = r"""
        PROGRAM HELLO_WORLD;
        
        VAR
        number, a, b, c: INTEGER;
        x: REAL;
        
        BEGIN
            BEGIN
                number := 2;
                a := number; { this is a comment }
                b := 10 * a + 10 * number DIV 4;
                c := a - - b
            END;
            x := 11.2;
        END.
        """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    SemanticAnalyzer().visit(tree)
    interpreter = Interpreter(tree)
    interpreter.interpret()

    assert interpreter.GLOBAL_SCOPE == {'A': 2, 'X': 11.2, 'C': 27, 'B': 25, 'NUMBER': 2}


def test_case_insensitive():
    text = r"""
        program hello_world;
        
        VAR
        _num_ber, a, b, c: INTEGER;
        x: integer;
        
        BEGIN

            BEgIN
                _num_ber := 2;
                a := _Num_Ber;
                B := 10 * a + 10 * _NUM_BER div 4;
                c := a - - b
            enD;
{ this is a comment }
        x := 11
        END.
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    SemanticAnalyzer().visit(tree)
    interpreter = Interpreter(tree)
    interpreter.interpret()

    assert interpreter.GLOBAL_SCOPE == {'A': 2, 'X': 11, 'C': 27, 'B': 25, '_NUM_BER': 2}


def test_part10():
    text = r"""
        PROGRAM Part10;
        VAR
          number : INTEGER;
          a, b, c, x : INTEGER;
          y : REAL;
        
        BEGIN
          {Part10}
        BEGIN
          number := 2;
          a := number;
          b := 10 * a + 10 * number DIV 4;
          c := a - - b
        END;
          x := 11;
          x := x / 2;
          y := 20 / 7 + 3.14;
          { writeln('a = ', a); }
          { writeln('b = ', b); }
          { writeln('c = ', c); }
          { writeln('number = ', number); }
          { writeln('x = ', x); }
          { writeln('y = ', y); }
        END.  {Part10}

    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    SemanticAnalyzer().visit(tree)
    interpreter = Interpreter(tree)
    interpreter.interpret()

    assert interpreter.GLOBAL_SCOPE == {'A': 2, 'C': 27, 'B': 25, 'NUMBER': 2, 'Y': 5.997142857142857, 'X': 5.5}


def test_symbol_table_builder():
    text = """
    PROGRAM Part11;
    VAR
       x : INTEGER;
       y : REAL;
    
    BEGIN
    
    END.
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SemanticAnalyzer()
    symtab_builder.visit(tree)

    assert symtab_builder.scope._symbols == {
        'INTEGER': integer_type,
        'REAL': real_type,
        'X': VarSymbol('X', integer_type),
        'Y': VarSymbol('Y', real_type)
    }


def test_symtab_exception1():
    text = """
    PROGRAM NameError1;
    VAR
       a : INTEGER;
    
    BEGIN
       a := 2 + b;
    END.
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SemanticAnalyzer()

    with pytest.raises(UndeclaredVariable) as e:
        symtab_builder.visit(tree)

    assert e.typename == 'UndeclaredVariable'
    assert e.value.message == "'B'"


def test_symtab_exception2():
    text = """
    PROGRAM NameError2;
    VAR
       b : INTEGER;
    
    BEGIN
       b := 1;
       a := b + 2;
    END.
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SemanticAnalyzer()

    with pytest.raises(UndeclaredVariable) as e:
        symtab_builder.visit(tree)

    assert e.typename == 'UndeclaredVariable'
    assert e.value.message == "'A'"


def test_part11():
    text = """
        PROGRAM Part11;
    VAR
       number : INTEGER;
       a, b   : INTEGER;
       y      : REAL;
    
    BEGIN {Part11}
       number := 2;
       a := number ;
       b := 10 * a + 10 * number DIV 4;
       y := 20 / 7 + 3.14
    END.  {Part11}
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SemanticAnalyzer()
    symtab_builder.visit(tree)
    interpreter = Interpreter(tree)
    interpreter.interpret()

    assert symtab_builder.scope._symbols == {
        'INTEGER': integer_type,
        'REAL': real_type,
        'NUMBER': VarSymbol('NUMBER', integer_type),
        'A': VarSymbol('A', integer_type),
        'B': VarSymbol('B', integer_type),
        'Y': VarSymbol('Y', real_type)
    }

    assert interpreter.GLOBAL_SCOPE == dict(A=2,
                                            B=25,
                                            NUMBER=2,
                                            Y=5.997142857142857)


def test_part12():
    text = """
    PROGRAM Part12;
    VAR
       a : INTEGER;
    
    PROCEDURE P1;
    VAR
       a : REAL;
       k : INTEGER;
    
       PROCEDURE P2;
       VAR
          a, z : INTEGER;
       BEGIN {P2}
          z := 777;
       END;  {P2}
    
    BEGIN {P1}
    
    END;  {P1}
    
    BEGIN {Part12}
       a := 10;
    END.  {Part12}
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SemanticAnalyzer()
    symtab_builder.visit(tree)
    interpreter = Interpreter(tree)
    interpreter.interpret()

    assert symtab_builder.scope._symbols == {
        'INTEGER': integer_type,
        'REAL': real_type,
        'A': VarSymbol('A', integer_type)
    }

    assert interpreter.GLOBAL_SCOPE == {'A': 10}


def test_duplicate_decl_error():
    text = """
    program SymTab6;
       var x, y : integer;
       var y : real;
    begin
       x := x + y;
    end.
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SemanticAnalyzer()

    with pytest.raises(DuplicateDeclaration) as e:
        symtab_builder.visit(tree)

    assert e.typename == 'DuplicateDeclaration'
    assert e.value.message == "'Y'"
