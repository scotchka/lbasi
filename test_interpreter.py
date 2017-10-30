from spi import Lexer, Parser, Interpreter


def test_interpreter():
    text = """
        BEGIN
            BEGIN
                number := 2;
                a := number;
                b := 10 * a + 10 * number / 4;
                c := a - - b
            END;
            x := 11;
        END.
        """

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

    assert interpreter.GLOBAL_SCOPE == {'a': 2, 'x': 11, 'c': 27, 'b': 25, 'number': 2}
