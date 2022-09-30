from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # расстояние, которое спортсмен преодолевает за один шаг
    M_IN_KM = 1000  # константа для перевода значений из метров в километры

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        km_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return km_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CAL_1 = 18
    COEFF_CAL_2 = 20

    def get_spent_calories(self) -> float:
        run_result = ((self.COEFF_CAL_1 * self.get_mean_speed()
                      - self.COEFF_CAL_2)
                      * self.weight / self.M_IN_KM * self.duration * 60)
        return run_result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        COEFF_WLK_1 = 0.035
        COEFF_WLK_2 = 0.029
        walk_result = (COEFF_WLK_1 * self.weight + (
                       self.get_mean_speed()**2 // self.height
                       ) * COEFF_WLK_2 * self.weight) * self.duration * 60
        return walk_result


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # один гребок при плавании — 1.38 метра
    COEFF_SWM_1 = 1.1
    COEFF_SWM_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        swimming_avg_speed = (self.length_pool * self.count_pool
                              / self.M_IN_KM / self.duration)
        return swimming_avg_speed

    def get_spent_calories(self) -> float:
        swim_result = (self.get_mean_speed() + self.COEFF_SWM_1
                       ) * self.COEFF_SWM_2 * self.weight
        return swim_result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    sensor_data = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return sensor_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

# От себя: Наталия, @dataclasses сильно приукрашает код
# А самое главное - радует что работает! =D
