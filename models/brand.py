from database.brand import BrandQueries

class Brand:
    def __init__(self, brand_data):
        self.db = BrandQueries()
        self.brand_data = brand_data

    def create_brand(self):
        self.db.create_brand(self.brand_data)

    def get_brand(self, id):
        return self.db.get_brand(id)
    
    def update_brand(self, id):
        self.db.update_brand(id, self.brand_data)

    def delete_brand(self, id):
        self.db.delete_brand(id)

    def get_all_brands(self):
        return self.db.get_all()

    def get_brands_by_type(self, type):
        return self.db.get_brands_by_type(type)

    def get_brands_by_industry(self, industry):
        return self.db.get_brands_by_industry(industry)

    def search_brands(self, keyword):
        return self.db.search_brands(keyword)

    def get_last_insert_id(self):
        return self.db.get_last_insert_id()
