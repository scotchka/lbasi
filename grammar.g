block: "{" (stmt ";") * "}"

stmt: "let" WORD expr -> assign
    | "fn" WORD "(" WORD * ")" block -> function
    | "return" expr -> return
    | "if" expr block ("elif" expr block)* ("else" block)? -> conditional
    | "print" expr -> print
    | expr
    

expr: expr ("<" | ">" | "==" | "<=" | ">=") expr -> compare
    | term ("+"|"-") expr -> add_sub
    | term
    
term: factor ("*"|"/") term -> mul_div
    | factor

factor: NUMBER
    | WORD
    | ESCAPED_STRING
    | WORD "(" expr* ")" -> call
    | "(" expr ")"

%import common.NUMBER
%import common.ESCAPED_STRING
%import common.WORD
%import common.WS
%ignore WS