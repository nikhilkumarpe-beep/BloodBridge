import sqlite3

def check_sqlite():
    conn = sqlite3.connect('instance/bloodbank.db')
    cursor = conn.cursor()
    
    phones = ['8105336328', '7483176991']
    for p in phones:
        cursor.execute("SELECT first_name, last_name, phone, blood_type, postal_code, is_donor FROM user WHERE phone = ?", (p,))
        row = cursor.fetchone()
        if row:
            print(f"Found: {row}")
        else:
            print(f"Not found: {p}")
            
    conn.close()

if __name__ == '__main__':
    check_sqlite()
