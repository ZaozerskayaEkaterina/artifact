from PIL import Image
import numpy as np
import math


def rotate_image_with_shift(image_path, angle, output_prefix):
    # Открываем изображение
    img = Image.open(image_path)
    img_array = np.array(img)

    # Преобразуем угол в радианы
    a = math.radians(angle)

    # Определяем матрицы сдвига
    shift_matrix1 = np.array([[1, -math.tan(a / 2), 0],
                              [0, 1, 0],
                              [0, 0, 1]])

    shift_matrix2 = np.array([[1, 0, 0],
                              [math.sin(a), 1, 0],
                              [0, 0, 1]])

    shift_matrix3 = np.array([[1, -math.tan(a / 2), 0],
                              [0, 1, 0],
                              [0, 0, 1]])

    # Список матриц для обработки
    matrices = [shift_matrix1, shift_matrix2, shift_matrix3]

    # Получаем размеры изображения
    height, width = img_array.shape[:2]
    center_x, center_y = width // 2, height // 2

    # Применяем сдвиги последовательно
    for i, matrix in enumerate(matrices):
        # Создаем временный массив для хранения промежуточных результатов
        temp_img_array = np.zeros_like(img_array)

        for x in range(img_array.shape[0]):
            for y in range(img_array.shape[1]):
                # Приводим координаты к однородным
                original_coords = np.array([x - center_x, y - center_y, 1])  # Центрируем координаты
                new_coords = matrix @ original_coords

                new_x = int(new_coords[0] + center_x)  # Возвращаем координаты обратно в исходную систему
                new_y = int(new_coords[1] + center_y)

                # Проверяем границы
                if 0 <= new_x < img_array.shape[0] and 0 <= new_y < img_array.shape[1]:
                    temp_img_array[new_x, new_y] = img_array[x, y]

        # Обновляем изображение для следующего сдвига
        img_array = temp_img_array.copy()

        # Сохраняем промежуточное изображение
        new_image = Image.fromarray(img_array)
        new_image.save(f"{output_prefix}_shifted_{i + 1}.png")


def rotate_image_with_turn(image_path, angle, output_prefix):
    # Открываем изображение
    img = Image.open(image_path)
    img_array = np.array(img)

    # Преобразуем угол в радианы
    a = math.radians(angle)

    # Определяем матрицу поворота
    turn_matrix = np.array([[math.cos(a), -math.sin(a), 0],
                                 [math.sin(a), math.cos(a), 0],
                                 [0, 0, 1]])

    # Получаем размеры изображения
    height, width = img_array.shape[:2]
    center_x, center_y = width // 2, height // 2

    # Создаем временный массив для хранения результатов поворота
    rotated_img_array = np.zeros_like(img_array)

    for x in range(img_array.shape[0]):
        for y in range(img_array.shape[1]):
            # Приводим координаты к однородным
            original_coords = np.array([x - center_x, y - center_y, 1])  # Центрируем координаты
            new_coords = turn_matrix @ original_coords

            new_x = int(new_coords[0] + center_x)  # Возвращаем координаты обратно в исходную систему
            new_y = int(new_coords[1] + center_y)

            # Проверяем границы
            if 0 <= new_x < img_array.shape[0] and 0 <= new_y < img_array.shape[1]:
                rotated_img_array[new_x, new_y] = img_array[x, y]

    # Сохраняем повернутое изображение
    rotated_image = Image.fromarray(rotated_img_array)
    rotated_image.save(f"{output_prefix}_turned.png")


in_path = "закат.png"
in_angle = 15  # Угол поворота в градусах 5, 15, 25

# Применяем аффинные трансформации сдвига
rotate_image_with_shift(in_path, in_angle, "output_image")

# Применяем аффинную трансформацию поворота
rotate_image_with_turn(in_path, in_angle, "output_image")