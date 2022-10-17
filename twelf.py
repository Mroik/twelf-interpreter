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

    def is_EOF(self) -> bool:
        if len(self._text) == 0:
            return True
        return False


class Lexer:
    def __init__(self, reader: InputReader):
        self._reader = reader
        self._queue = []

    def _generate_token(self):
        accumulator = []
        while not True:
            match self._reader.peek():
                case ":":
                    if len(accumulator) == 0:
                        accumulator.append(self._reader.consume())
                    break
                case " ":
                    self._reader.consume()
                    if len(accumulator) != 0:
                        break
                case ".":
                    accumulator.append(self._reader.consume())
                    break
                case _:
                    accumulator.append(self._reader.consume())
        return "".join(accumulator)


    def peek(self, k: int = 1) -> List[str]:
        l_queue = len(self._queue)
        if k < l_queue:
            for x in range(k - l_queue):
                self._queue.append(self._generate_token())
        return self._queue[:k]

    def consume(self, k: int = 1) -> List[str]:
        self.peek(k)
        ris = self._queue[:k]
        self._queue = self._queue[k:]
        return ris


class Parser:
    def __init__(self):
        self._grammar = None

    def parse(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
