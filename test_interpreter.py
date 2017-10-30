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

    assert interpreter.GLOBAL_SCOPE == {'A': 2, 'X': 11, 'C': 27, 'B': 25, 'NUMBER': 2}


def test_case_insensitive():
    text = """
        BEGIN

            BEgIN
                number := 2;
                a := NumBer;
                B := 10 * a + 10 * NUMBER / 4;
                c := a - - b
            enD;

        x := 11;
        END.
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

    assert interpreter.GLOBAL_SCOPE == {'A': 2, 'X': 11, 'C': 27, 'B': 25, 'NUMBER': 2}
