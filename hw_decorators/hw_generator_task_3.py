"""
Доработать функцию flat_generator.
Должен получиться генератор, который принимает список списков и возвращает их плоское представление.
Функция test в коде ниже также должна отработать без ошибок.
"""

import types
from logger_params_task_2 import logger

# ========== Применяем логгер к генератору из предыдущего ДЗ ==========
@logger('generator.log')  # логи будем сохранять в generator.log
def flat_generator(list_of_lists):
    # Проходим по каждому подсписку во внешнем списке
    for sublist in list_of_lists:
        # Проходим по каждому элементу внутри подсписка и возвращаем его
        for item in sublist:
            yield item


# ========== Тест (без изменений) ==========
def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
