from models.car import Car

class Inventory:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.cars_data = self.file_handler.load_data("cars")
        self.cars = {car_id: Car.from_dict(data) for car_id, data in self.cars_data.items()}

    def _save(self):
        data = {car_id: car.to_dict() for car_id, car in self.cars.items()}
        self.file_handler.save_data("cars", data)

    def add_car(self, car):
        if car.car_id in self.cars:
            raise ValueError(f"Car with ID {car.car_id} already exists.")
        self.cars[car.car_id] = car
        self._save()

    def update_car(self, car_id, **kwargs):
        if car_id not in self.cars:
            raise ValueError(f"Car with ID {car_id} not found.")
        car = self.cars[car_id]
        for key, value in kwargs.items():
            if hasattr(car, key):
                setattr(car, key, value)
        self._save()

    def remove_car(self, car_id):
        if car_id not in self.cars:
            raise ValueError(f"Car with ID {car_id} not found.")
        del self.cars[car_id]
        self._save()

    def get_car(self, car_id):
        return self.cars.get(car_id)

    def get_all_cars(self):
        return list(self.cars.values())

    def filter_cars(self, category=None, status=None, max_price=None):
        result = self.get_all_cars()
        if category:
            result = [c for c in result if c.category.lower() == category.lower()]
        if status:
            result = [c for c in result if c.status.lower() == status.lower()]
        if max_price is not None:
            result = [c for c in result if c.rental_price_per_day <= max_price]
        return result
