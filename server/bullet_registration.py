import math


def are_points_collinear(x1, y1, x2, y2, x3, y3, tolerance_percent=3):
    """
    Проверяет, лежат ли три точки на одной прямой с заданной погрешностью.

    Args:
        x1, y1: первая точка
        x2, y2: вторая точка
        x3, y3: третья точка
        tolerance_percent: допустимая погрешность в процентах (по умолчанию 3%)

    Returns:
        bool: True если точки коллинеарны в пределах погрешности, иначе False
    """
    # Вычисляем площадь треугольника по трем точкам
    # Формула: area = |(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2|
    area = abs(
        x1 * (y2 - y3) +
        x2 * (y3 - y1) +
        x3 * (y1 - y2)
    ) / 2.0

    # Если площадь очень маленькая - точки коллинеарны
    # Вычисляем максимально возможную площадь для этих точек
    # Используем длины сторон как базовую линию

    # Вычисляем длины сторон
    d12 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    d13 = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)
    d23 = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)

    # Находим максимальное расстояние для масштабирования
    max_distance = max(d12, d13, d23)

    # Избегаем деления на ноль
    if max_distance == 0:
        return True  # все точки совпадают

    # Преобразуем процент погрешности в абсолютное значение
    tolerance = tolerance_percent / 100.0 * max_distance

    # Рассчитываем "высоту" треугольника, которая должна быть меньше погрешности
    # Высота = 2 * площадь / основание
    # Используем самую длинную сторону как основание
    if d12 >= d13 and d12 >= d23:
        base = d12
    elif d13 >= d12 and d13 >= d23:
        base = d13
    else:
        base = d23

    height = 2 * area / base if base > 0 else 0

    return height <= tolerance


async def bullet_registration(start_pos_x, start_pos_y, target_pos_x, target_pos_y, players_list):
    """
    Проверяет, какие игроки находятся на линии выстрела
    """
    hit_players = []

    for player_id, player_data in players_list.items():
        # Получаем координаты игрока
        player_x = player_data["x"]
        player_y = player_data["y"]

        # Проверяем коллинеарность трех точек:
        # 1. Начало выстрела (start_pos_x, start_pos_y)
        # 2. Цель выстрела (target_pos_x, target_pos_y)
        # 3. Игрок (player_x, player_y)
        if are_points_collinear(
                start_pos_x, start_pos_y,
                target_pos_x, target_pos_y,
                player_x, player_y,
                tolerance_percent=3
        ):
            hit_players.append(player_id)
            print(f"Игрок {player_id} на линии выстрела!")

    return hit_players