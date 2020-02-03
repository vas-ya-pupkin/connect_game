import numpy as np
import itertools
from typing import Iterator

np.set_printoptions(threshold=np.inf)


class Game:
    EMPTY = 'X'
    PLAYERS = {
        1: '●',
        2: '○',
    }
    WINNING_LENGTH = 4  # длина ряда для победы

    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.field = np.chararray((rows, columns), unicode=True)
        self.field.fill(self.EMPTY)

        self.turn_generator = self.turn()
        self.current_player = self._change_turn()

        self.finished = False

    def turn(self) -> Iterator[int]:
        """
        Возвращает номер игрока, чья очередь ходить
        :return:
        """
        while True:
            for player in self.PLAYERS.keys():
                yield player

    def draw(self) -> None:
        """
        Вывод игрового поля
        :return:
        """
        drawable = self._prepare_field_for_drawing()
        print(drawable)
        print()

    def _prepare_field_for_drawing(self) -> str:
        return '\n'.join(
            [
                ' '.join(row) for
                row in self.field
            ]
        )

    def new_turn(self, row: int, column: int) -> bool:
        """
        Осуществление хода
        :param row:
        :param column:
        :return:
        """
        if self.finished:
            raise RuntimeError('Игра окончена')

        row, column = self._user_input_to_machine(row, column)
        if any([row < 0, column < 0, row > self.rows, column > self.columns]):
            raise ValueError(f'Допустимые значения: 1-{self.rows}, 1-{self.columns}')

        real_row = self._gravity(row, column)
        if real_row == -1:
            raise ValueError('Этот столбец полностью занят')

        self._set_new_dot(real_row, column)

        if self._is_current_player_a_winner():
            self.finished = True
            self._congrats()

        self.current_player = self._change_turn()
        return True

    def _congrats(self) -> None:
        print(f"Игрок {self.current_player} победил!")

    def _gravity(self, row: int, column: int):
        """
        Возвращает номер строки, до которой падает шар
        :param row:
        :param column:
        :return:
        """
        real_row = -1
        for i in range(row - 1, self.rows)[::-1]:
            if self.field[i][column] == self.EMPTY:
                real_row = i
                break
        return real_row

    def _set_new_dot(self, row: int, column: int) -> None:
        """
        Вставка символа игрока в поле
        :param row:
        :param column:
        :return:
        """
        self.field[row][column] = self.PLAYERS[self.current_player]

    def _change_turn(self) -> int:
        """
        Изменение текущего игрока
        :return:
        """
        return next(self.turn_generator)

    def _is_current_player_a_winner(self) -> bool:
        """
        Есть ли на поле последовательность достаточной для победы длины
        :return:
        """
        for row in self.field.tolist() + np.rot90(self.field).tolist():
            lenghts = [
                len(list(x[1])) for x in
                itertools.groupby(row) if
                x[0] == self.PLAYERS[self.current_player]
            ]  # длина всех последовательностей символов текущего игрока
            if not lenghts:
                continue
            if max(lenghts) >= self.WINNING_LENGTH:
                return True
        return False

    @property
    def player(self):
        return self.current_player

    @property
    def is_finished(self):
        return self.finished

    @staticmethod
    def _user_input_to_machine(row: int, column: int):
        """
        Преобразование ввода пользователя, который считает клетки с единицы, в индексы массива (с нуля)
        :param row:
        :param column:
        :return:
        """
        return row - 1, column - 1
