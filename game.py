import pygame
# Импортируем класс Board из нашего пакета
from gameparts import Board

def save_result(result):
    with open('results.txt', 'a', encoding='utf-8') as file:
        file.write(result + '\n')

pygame.init()

# Константы для оформления
CELL_SIZE = 100
BOARD_SIZE = 3
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE
LINE_WIDTH = 15
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)
X_WIDTH = 15
O_WIDTH = 15
SPACE = CELL_SIZE // 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Крестики-нолики')
screen.fill(BG_COLOR)

def draw_lines():
    # Горизонтальные линии
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen, LINE_COLOR,
            (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH
        )
    # Вертикальные линии
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen, LINE_COLOR,
            (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH
        )

def draw_figures(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                # Рисуем две линии для крестика
                pygame.draw.line(
                    screen, X_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE),
                    (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE),
                    X_WIDTH
                )
                pygame.draw.line(
                    screen, X_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE),
                    (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE),
                    X_WIDTH
                )
            elif board[row][col] == 'O':
                # Рисуем круг для нолика
                pygame.draw.circle(
                    screen, O_COLOR,
                    (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                    CELL_SIZE // 2 - SPACE, O_WIDTH
                )

def main():
    game = Board()
    current_player = 'X'
    running = True
    
    # Сразу рисуем сетку
    draw_lines()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Получаем координаты клика
                mouse_y = event.pos[0]
                mouse_x = event.pos[1]

                clicked_row = mouse_x // CELL_SIZE
                clicked_col = mouse_y // CELL_SIZE

                # Проверяем, свободна ли ячейка
                if game.board[clicked_row][clicked_col] == ' ':
                    # Делаем ход
                    game.make_move(clicked_row, clicked_col, current_player)
                    
                    # Проверяем победу
                    if game.check_win(current_player):
                        result = f'Победили {current_player}.'
                        print(result)
                        save_result(result)
                        running = False
                    
                    # Проверяем ничью
                    elif game.is_board_full():
                        result = 'Ничья!'
                        print(result)
                        save_result(result)
                        running = False
                    
                    # Передаем ход
                    current_player = 'O' if current_player == 'X' else 'X'
                    
                    # Отрисовываем обновленное поле
                    draw_figures(game.board)
        
        pygame.display.update()
    
    # Небольшая пауза перед закрытием, чтобы увидеть финальный ход
    pygame.time.wait(1000)
    pygame.quit()

if __name__ == '__main__':
    main()