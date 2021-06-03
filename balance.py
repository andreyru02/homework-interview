from stack import Stack


class Balance:
    def __init__(self):
        self.stack = Stack()
        self.opens = '({['
        self.closes = ')}]'

    def balance(self, symbols):
        for symb in symbols:
            if symb in self.opens:
                self.stack.push(self.opens.index(symb))
            else:
                if self.stack.stack and self.stack.peek() == self.closes.index(symb):
                    self.stack.pop()
                else:
                    return 'Несбалансированно'

        return 'Сбалансированно'


if __name__ == '__main__':
    balance = Balance()
    print(balance.balance('(((([{}]))))'))
    print(balance.balance('[([])((([[[]]])))]{()}'))
    print(balance.balance('{{[()]}}'))
    print(balance.balance('}{}'))
    print(balance.balance('{{[(])]}}'))
    print(balance.balance('[[{())}]'))
