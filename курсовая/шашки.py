from tkinter import *
from tkinter import messagebox
import random
import time
import copy

gen_win = Tk()  # создаём окно
gen_win.title('Шашки')  # заголовок окна
deck = Canvas(gen_win, width=800, height=800, bg='#ffeba9')
deck.pack()

n2_list = ()  # конечный список ходов компьютера
ur = 3  # количество предсказываемых компьютером ходов
k_res = 0  # !!!
o_res = 0
pos1x = -1  # клетка не задана
f_hi = True  # определение хода игрока(да)


def imagesofpewki():  # загружаем изображения пешек
    global pewki
    i1 = PhotoImage(file="wh.gif")
    i2 = PhotoImage(file="whd.gif")
    i3 = PhotoImage(file="bl.gif")
    i4 = PhotoImage(file="bld.gif")
    pewki = [0, i1, i2, i3, i4]


def new_game():  # начинаем новую игру
    global field
    field = [[0, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 3, 0, 3, 0, 3, 0],
            [0, 3, 0, 3, 0, 3, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]]


def pin(x_poz_1, y_poz_1, x_poz_2, y_poz_2):  # рисуем игровое поле
    global pewki
    global field
    global redframe, greenframe
    k = 100
    x = 0
    deck.delete('all')
    redframe = deck.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    greenframe = deck.create_rectangle(-5, -5, -5, -5, outline="green", width=5)

    while x < 8 * k:  # рисуем доску
        y = 1 * k
        while y < 8 * k:
            deck.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k
    while x < 8 * k:  # рисуем доску
        y = 0
        while y < 8 * k:
            deck.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k

    for y in range(8):  # рисуем стоячие пешки
        for x in range(8):
            z = field[y][x]
            if z:
                if (x_poz_1, y_poz_1) != (x, y):  # стоячие пешки?
                    deck.create_image(x * k, y * k, anchor=NW, image=pewki[z])
    # рисуем активную пешку
    z = field[y_poz_1][x_poz_1]
    if z:  # ???
        deck.create_image(x_poz_1 * k, y_poz_1 * k, anchor=NW, image=pewki[z], tag='ani')
    # вычисление коэф. для анимации
    kx = 1 if x_poz_1 < x_poz_2 else -1
    ky = 1 if y_poz_1 < y_poz_2 else -1
    for i in range(abs(x_poz_1 - x_poz_2)):  # анимация перемещения пешки
        for ii in range(33):
            deck.move('ani', 0.03 * k * kx, 0.03 * k * ky)
            deck.update()  # обновление
            time.sleep(0.01)


def messagg(s):
    global f_hi
    z = 'Игра завершена'
    if s == 1:
        i = messagebox.askyesno(title=z, message='You won!\nPress "Yes" to strart game again.', icon='info')
    if s == 2:
        i = messagebox.askyesno(title=z, message='You lose!\nPress "Yes" to strart game again.', icon='info')
    if s == 3:
        i = messagebox.askyesno(title=z, message='There are no more moves.\nPress "Yes" to strart game again.', icon='info')
    if i:
        new_game()
        pin(-1, -1, -1, -1)  # рисуем игровое поле
        f_hi = True  # ход игрока доступен


def pos1(event):  # выбор клетки для хода 1
    x, y = (event.x) // 100, (event.y) // 100  # вычисляем координаты клетки
    deck.coords(greenframe, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке


def pos2(event):  # выбор клетки для хода 2
    global pos1x, pos1y, pos2x, pos2y
    global f_hi
    x, y = (event.x) // 100, (event.y) // 100  # вычисляем координаты клетки
    if field[y][x] == 1 or field[y][x] == 2:  # проверяем пешку игрока в выбранной клетке
        deck.coords(redframe, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке
        pos1x, pos1y = x, y
    else:
        if pos1x != -1:  # клетка выбрана
            pos2x, pos2y = x, y
            if f_hi:  # ход игрока?
                playersmove()
                if not (f_hi):
                    time.sleep(0.5)
                    computersmove()  # передаём ход компьютеру
                    # gl_okno.after(500,hod_kompjutera(0))#!!!#передаём ход компьютеру
            pos1x = -1  # клетка не выбрана
            deck.coords(redframe, -5, -5, -5, -5)  # рамка вне поля


def computersmove():  # !!!
    global f_hi
    global n2_list
    checkcm(1, (), [])
    if n2_list:  # проверяем наличие доступных ходов
        kh = len(n2_list)  # количество ходов
        th = random.randint(0, kh - 1)  # случайный ход
        dh = len(n2_list[th])  # длина хода
        for h in n2_list:  # !!!для отладки!!!
            h = h  # !!!для отладки!!!
        for i in range(dh - 1):
            # выполняем ход
            spisok = move(1, n2_list[th][i][0], n2_list[th][i][1], n2_list[th][1 + i][0], n2_list[th][1 + i][1])
        n2_list = []  # очищаем список ходов
        f_hi = True  # ход игрока доступен

    # определяем победителя
    s_k, s_i = skan()
    if not (s_i):
        messagg(2)
    elif not (s_k):
        messagg(1)
    elif f_hi and not (listpm()):
        messagg(3)
    elif not (f_hi) and not (listcm()):
        messagg(3)


def listcm():  # составляем список ходов компьютера
    spisok = movelookc1([])  # здесь проверяем обязательные ходы
    if not (spisok):
        spisok = movelookc2([])  # здесь проверяем оставшиеся ходы
    return spisok


def checkcm(tur, n_list, spisok):  # !!!
    global field
    global n2_list
    global l_res, k_res, o_res
    if not (spisok):  # если список ходов пустой...
        spisok = listcm() # заполняем

    if spisok:
        k_field = copy.deepcopy(field)  # копируем поле
        for ((pos1x, pos1y), (pos2x, pos2y)) in spisok:  # проходим все ходы по списку
            t_list = move(0, pos1x, pos1y, pos2x, pos2y)
            if t_list:  # если существует ещё ход
                checkcm(tur, (n_list + ((pos1x, pos1y),)), t_list)
            else:
                checkpm(tur, [])
                if tur == 1:
                    t_res = o_res / k_res
                    if not (n2_list):  # записыаем если пустой
                        n2_list = (n_list + ((pos1x, pos1y), (pos2x, pos2y)),)
                        l_res = t_res  # сохряняем наилучший результат
                    else:
                        if t_res == l_res:
                            n2_list = n2_list + (n_list + ((pos1x, pos1y), (pos2x, pos2y)),)
                        if t_res > l_res:
                            n2_list = ()
                            n2_list = (n_list + ((pos1x, pos1y), (pos2x, pos2y)),)
                            l_res = t_res  # сохряняем наилучший результат
                    o_res = 0
                    k_res = 0

            field = copy.deepcopy(k_field)  # возвращаем поле
    else:  # ???
        s_k, s_i = skan()  # подсчёт результата хода
        o_res += (s_k - s_i)
        k_res += 1


def listpm():  # составляем список ходов игрока
    spisok = movelookp1([])  # здесь проверяем обязательные ходы
    if not (spisok):
        spisok = movelookp2([])  # здесь проверяем оставшиеся ходы
    return spisok


def checkpm(tur, spisok):
    global field, k_res, o_res
    global ur
    if not (spisok):
        spisok = listpm()

    if spisok:  # проверяем наличие доступных ходов
        k_field = copy.deepcopy(field)  # копируем поле
        for ((pos1x, pos1y), (pos2x, pos2y)) in spisok:
            t_list = move(0, pos1x, pos1y, pos2x, pos2y)
            if t_list:  # если существует ещё ход
                checkpm(tur, t_list)
            else:
                if tur < ur:
                    checkcm(tur + 1, (), [])
                else:
                    s_k, s_i = skan()  # подсчёт результата хода
                    o_res += (s_k - s_i)
                    k_res += 1

            field = copy.deepcopy(k_field)  # возвращаем поле
    else:  # доступных ходов нет
        s_k, s_i = skan()  # подсчёт результата хода
        o_res += (s_k - s_i)
        k_res += 1


def skan():  # подсчёт пешек на поле
    global field
    s_i = 0
    s_k = 0
    for i in range(8):
        for ii in field[i]:
            if ii == 1: s_i += 1
            if ii == 2: s_i += 3
            if ii == 3: s_k += 1
            if ii == 4: s_k += 3
    return s_k, s_i


def playersmove():
    global pos1x, pos1y, pos2x, pos2y
    global f_hi
    f_hi = False  # считаем ход игрока выполненным
    spisok = listpm()
    if spisok:
        if ((pos1x, pos1y), (pos2x, pos2y)) in spisok:  # проверяем ход на соответствие правилам игры
            t_list = move(1, pos1x, pos1y, pos2x, pos2y)  # если всё хорошо, делаем ход
            if t_list:  # если есть ещё ход той же пешкой
                f_hi = True  # считаем ход игрока невыполненным
        else:
            f_hi = True  # считаем ход игрока невыполненным
    deck.update()  # !!!обновление


def move(f, pos1x, pos1y, pos2x, pos2y):
    global field
    if f: pin(pos1x, pos1y, pos2x, pos2y)  # рисуем игровое поле
    # превращение
    if pos2y == 0 and field[pos1y][pos1x] == 1:
        field[pos1y][pos1x] = 2
    # превращение
    if pos2y == 7 and field[pos1y][pos1x] == 3:
        field[pos1y][pos1x] = 4
    # делаем ход
    field[pos2y][pos2x] = field[pos1y][pos1x]
    field[pos1y][pos1x] = 0

    # рубим пешку игрока
    kx = ky = 1
    if pos1x < pos2x: kx = -1
    if pos1y < pos2y: ky = -1
    xpos, ypos = pos2x, pos2y
    while (pos1x != xpos) or (pos1y != ypos):
        xpos += kx
        ypos += ky
        if field[ypos][xpos] != 0:
            field[ypos][xpos] = 0
            if f: pin(-1, -1, -1, -1)  # рисуем игровое поле
            # проверяем ход той же пешкой...
            if field[pos2y][pos2x] == 3 or field[pos2y][pos2x] == 4:  # ...компьютера
                return movelookc1p([], pos2x, pos2y)  # возвращаем список доступных ходов
            elif field[pos2y][pos2x] == 1 or field[pos2y][pos2x] == 2:  # ...игрока
                return movelookp1p([], pos2x, pos2y)  # возвращаем список доступных ходов
    if f: pin(pos1x, pos1y, pos2x, pos2y)  # рисуем игровое поле


def movelookc1(spisok):  # проверка наличия обязательных ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            spisok = movelookc1p(spisok, x, y)
    return spisok


def movelookc1p(spisok, x, y):
    if field[y][x] == 3:  # пешка
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                    if field[y + iy + iy][x + ix + ix] == 0:
                        spisok.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
    if field[y][x] == 4:  # пешка с короной
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0  # определение правильности хода
            for i in range(1, 8):
                if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                    if osh == 1:
                        spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                    if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2:
                        osh += 1
                    if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4 or osh == 2:
                        if osh > 0: spisok.pop()  # удаление хода из списка
                        break
    return spisok


def movelookc2(spisok):  # проверка наличия остальных ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            if field[y][x] == 3:  # пешка
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if field[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                        if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    spisok.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))  # запись хода в конец списка
            if field[y][x] == 4:  # пешка с короной
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0  # определение правильности хода
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if field[y + iy * i][x + ix * i] == 0:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                            if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4 or osh == 2:
                                break
    return spisok


def movelookp1(spisok):  # проверка наличия обязательных ходов
    spisok = []  # список ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            spisok = movelookp1p(spisok, x, y)
    return spisok


def movelookp1p(spisok, x, y):
    if field[y][x] == 1:  # пешка
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                    if field[y + iy + iy][x + ix + ix] == 0:
                        spisok.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
    if field[y][x] == 2:  # пешка с короной
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0  # определение правильности хода
            for i in range(1, 8):
                if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                    if osh == 1:
                        spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                    if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4:
                        osh += 1
                    if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2 or osh == 2:
                        if osh > 0: spisok.pop()  # удаление хода из списка
                        break
    return spisok


def movelookp2(spisok):  # проверка наличия остальных ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            if field[y][x] == 1:  # пешка
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if field[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                        if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    spisok.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))  # запись хода в конец списка
            if field[y][x] == 2:  # пешка с короной
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0  # определение правильности хода
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if field[y + iy * i][x + ix * i] == 0:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                            if field[y + iy * i][x + ix * i] == 3 or field[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if field[y + iy * i][x + ix * i] == 1 or field[y + iy * i][x + ix * i] == 2 or osh == 2:
                                break
    return spisok


imagesofpewki()  # здесь загружаем изображения пешек
new_game()  # начинаем новую игру
pin(-1, -1, -1, -1)  # рисуем игровое поле
deck.bind("<Motion>", pos1)  # движение мышки по полю
deck.bind("<Button-1>", pos2)  # нажатие левой кнопки

mainloop()
