import pytest
from spi import Lexer, Parser, Interpreter, SymbolTableBuilder


def test_interpreter():
    text = r"""
        PROGRAM HELLO_WORLD;
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
    interpreter = Interpreter(tree)
    interpreter.interpret()

    assert interpreter.GLOBAL_SCOPE == {'A': 2, 'X': 11.2, 'C': 27, 'B': 25, 'NUMBER': 2}


def test_case_insensitive():
    text = r"""
        program hello_world;
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
    symtab_builder = SymbolTableBuilder()
    symtab_builder.visit(tree)

    assert repr(symtab_builder.symtab) == 'Symbols: [INTEGER, REAL, <X: INTEGER>, <Y: REAL>]'

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
    symtab_builder = SymbolTableBuilder()

    with pytest.raises(NameError) as e:
        symtab_builder.visit(tree)

    assert e.typename == 'NameError'
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
    symtab_builder = SymbolTableBuilder()

    with pytest.raises(NameError) as e:
        symtab_builder.visit(tree)

    assert e.typename == 'NameError'
    assert e.value.message == "'A'"
