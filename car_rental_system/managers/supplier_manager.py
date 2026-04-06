from models.supplier import Supplier

class SupplierManager:
    def __init__(self, file_handler, inventory_manager):
        self.file_handler = file_handler
        self.inventory = inventory_manager
        
        self.suppliers_data = self.file_handler.load_data("suppliers")
        self.suppliers = {s_id: Supplier.from_dict(data) for s_id, data in self.suppliers_data.items()}

    def _save(self):
        data = {s_id: sup.to_dict() for s_id, sup in self.suppliers.items()}
        self.file_handler.save_data("suppliers", data)

    def add_supplier(self, supplier):
        if supplier.supplier_id in self.suppliers:
            raise ValueError(f"Supplier with ID {supplier.supplier_id} already exists.")
        self.suppliers[supplier.supplier_id] = supplier
        self._save()

    def add_car_from_supplier(self, supplier_id, car):
        if supplier_id not in self.suppliers:
            raise ValueError(f"Supplier with ID {supplier_id} not found.")
        self.inventory.add_car(car)
        self.suppliers[supplier_id].add_car_supplied(car.car_id)
        self._save()

    def get_supplier(self, supplier_id):
        return self.suppliers.get(supplier_id)

    def get_all_suppliers(self):
        return list(self.suppliers.values())
