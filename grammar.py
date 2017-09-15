from lark import Lark

with open('grammar.g') as f:
    grammar = f.read()
    
# print grammar

parser = Lark(grammar, start='block')

print parser.parse("""
{

fn fac(n) {
    if n < 2 {
        return 1;
    }
    else {
        return n * fac(n - 1);
    };
};

print fac(4);

fn fib(n) {};

}
""").pretty()
