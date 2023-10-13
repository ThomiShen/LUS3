import pymysql

class LoveDatabase:
    def __init__(self, host,port, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS LoveDB (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    gender VARCHAR(50),
                    age INT,
                    job VARCHAR(255),
                    house VARCHAR(255),
                    car VARCHAR(255),
                    interest VARCHAR(255),
                    location VARCHAR(255),
                    visual_age INT,
                    beauty FLOAT,
                    image  Blob
                )
            """)
            self.connection.commit()

    def insert_data(self, name, gender, age, fach,job, house, car, interest, location, visual_age, beauty,image,home,fang,evaluation):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO LoveDB (name, gender, age, fach,job, house, car, interest, location, visual_age, beauty,image,home,fang,evaluation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
            """, (name, gender, age,fach, job, house, car, interest, location, visual_age, beauty,image,home,fang,evaluation))
            self.connection.commit()

    def update_data(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                ALTER TABLE LoveDB MODIFY image MEDIUMBLOB;
            """)
            self.connection.commit()

    def fetch_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM LoveDB")
            return cursor.fetchall()

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    # 测试代码
    db = LoveDatabase(host='localhost', port=3306,user='root', password='12345678', database='test')
    db.update_data()
    db.close()
