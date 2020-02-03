from game import Game

if __name__ == '__main__':
    game = Game(6, 7)
    game.draw()

    while not game.is_finished:
        try:
            col, row = input(f'Ход игрока {game.player}. \n'
                             f'Координаты (строка столбец) > ').strip().split(' ')
            col = int(col)
            row = int(row)
        except ValueError:
            continue

        try:
            game.new_turn(col, row)
            game.draw()
        except (ValueError, RuntimeError) as e:
            print(str(e))
