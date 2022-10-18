from typing import List


class InputReader:
    def __init__(self, text: str):
        self._text = text
        self._index = 0

    def peek(self, k: int = 1) -> str:
        return self._text[self._index:self._index + k]

    def consume(self, k: int = 1) -> str:
        ris = self._text[self._index:self._index + k]
        self._text = self._text[self._index + k:]
        return ris

    def consume_up_to(self, token: str):
        index = self._text.find(token, self._index)
        self._index = index + len(token)

    def is_EOF(self) -> bool:
        if len(self._text) == 0:
            return True
        return False


class Lexer:
    def __init__(self, reader: InputReader):
        self._reader = reader
        self._queue = list()

    def _generate_token(self):
        accumulator = list()
        i = 1
        while True:
            try:
                match peeked := self._reader.peek(i)[i - 1]:
                    case ":":
                        if len(accumulator) == 0:
                            accumulator.append(peeked)
                            i += 1
                        break
                    case " ":
                        i += 1
                        if len(accumulator) != 0:
                            break
                    case ".":
                        accumulator.append(peeked)
                        i += 1
                        break
                    case "(":
                        if len(accumulator) == 0:
                            accumulator.append(peeked)
                            i += 1
                        break
                    case ")":
                        if len(accumulator) == 0:
                            accumulator.append(peeked)
                            i += 1
                        break
                    case _:
                        accumulator.append(peeked)
                        i += 1
            except IndexError:
                i += 1
                break
        return "".join(accumulator)


    def peek(self, k: int = 1) -> List[str]:
        l_queue = len(self._queue)
        if l_queue < k:
            for x in range(k - l_queue):
                generated = self._generate_token()
                self._queue.append(generated)
                self._reader.consume_up_to(generated)
        return self._queue[:k]

    def consume(self, k: int = 1) -> List[str]:
        self.peek(k)
        ris = self._queue[:k]
        self._queue = self._queue[k:]
        return ris


class Parser:
    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._types = list()
        self._functions = {}
        self._rules = {}

    # Does not support polymorphism
    def _parse_type_definition(self):
        if self._lexer.peek()[0] in self._types:
            raise Exception("TODO")
        self._types.append(self._lexer.consume(4)[0])

    # Does not support infixing
    def _parse_function_definiton(self):
        parameters = list()
        name = self._lexer.consume()[0]  # TODO check if already exist
        if self._lexer.consume()[0] != ":":
            raise Exception("TODO")
        while True:
            parameters.append(self._lexer.consume()[0])
            ender = self._lexer.consume()[0]
            if ender == ".":
                break
            if ender != "->":
                raise Exception("TODO")
        self._functions[name] = parameters

    def _parse_rule_definition(self):
        steps = list()
        name = self._lexer.consume(2)[0]
        i = 1
        while True:
            if self._lexer.peek(i)[i - 1] == "<-" or ".":
                # TODO check if function matches any existing ones
                pass

    def _parse_expression(self):
        pass

    def parse(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
