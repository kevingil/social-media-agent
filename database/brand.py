from sqlite3 import connect

class BrandQueries:
    def __init__(self):
        self._connection = connect("./database.db")
        self._cursor = self._connection.cursor()

    def get_all(self):
        data = self._cursor.execute("SELECT * FROM product_brand")
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_brand(self, id):
        brand = self._cursor.execute(f"SELECT * FROM product_brand WHERE id = ?", (id,))
        columns = [column[0] for column in brand.description]
        return dict(zip(columns, brand.fetchone()))

    def create_brand(self, brand):
        self._cursor.execute(
            """INSERT INTO product_brand (name, type, description, industry, website_url, location, target_audience, mission_statement, unique_selling_proposition, competitors, product_categories, distribution_channels, key_values)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (brand['name'], brand['type'], brand['description'], brand['industry'], brand['website_url'], brand['location'], brand['target_audience'], brand['mission_statement'], brand['unique_selling_proposition'], brand['competitors'], brand['product_categories'], brand['distribution_channels'], brand['key_values'])
        )
        self._connection.commit()

    def update_brand(self, id, brand):
        self._cursor.execute(
            """UPDATE product_brand SET name = ?, type = ?, description = ?, industry = ?, website_url = ?, location = ?, target_audience = ?, mission_statement = ?, unique_selling_proposition = ?, competitors = ?, product_categories = ?, distribution_channels = ?, key_values = ?
            WHERE id = ?""",
            (brand['name'], brand['type'], brand['description'], brand['industry'], brand['website_url'], brand['location'], brand['target_audience'], brand['mission_statement'], brand['unique_selling_proposition'], brand['competitors'], brand['product_categories'], brand['distribution_channels'], brand['key_values'], id)
        )
        self._connection.commit()

    def delete_brand(self, id):
        self._cursor.execute("DELETE FROM product_brand WHERE id = ?", (id,))
        self._connection.commit()

    def get_brands_by_type(self, type):
        data = self._cursor.execute("SELECT * FROM product_brand WHERE type = ?", (type,))
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_brands_by_industry(self, industry):
        data = self._cursor.execute("SELECT * FROM product_brand WHERE industry = ?", (industry,))
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def search_brands(self, keyword):
        data = self._cursor.execute("SELECT * FROM product_brand WHERE name LIKE ? OR description LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_last_insert_id(self):
        return self._cursor.lastrowid

    def __del__(self):
        self._connection.close()
