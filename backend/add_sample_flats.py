import pymysql

def add_sample_flats():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Singh@123',
        # only change this password
        database='rental_portal',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    cursor = conn.cursor()
    
    sample_flats = [
        ('A101', 25000, 'Sector 15, Noida', True, 2, 2, 1200, True, True, True, False, True),
        ('A102', 30000, 'Sector 18, Noida', True, 3, 2, 1500, True, True, False, True, True),
        ('B201', 22000, 'Sector 22, Noida', True, 2, 1, 1000, False, True, True, False, False),
        ('B202', 35000, 'Sector 25, Noida', True, 3, 3, 1800, True, True, True, True, True),
        ('C301', 28000, 'Sector 30, Noida', True, 2, 2, 1300, True, False, True, True, False)
    ]
    
    for flat in sample_flats:
        try:
            cursor.execute('''
                INSERT INTO flats (flat_no, rent, location, available, bedrooms, bathrooms, 
                                 area_sqft, swimming_pool, car_parking, bike_parking, gym, garden)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', flat)
        except pymysql.IntegrityError:
            print(f"Flat {flat[0]} already exists")
    
    conn.commit()
    conn.close()
    print("Sample flats added successfully!")

if __name__ == '__main__':
    add_sample_flats()