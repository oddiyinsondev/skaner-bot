import sqlite3

def check_and_add_tolov(telegram_id: int, code_id: int) -> bool:
    """code_id ni tekshiradi va kerak bo'lsa tolov jadvaliga ma'lumot qo'shadi"""
    try:
        conn = sqlite3.connect('apteka.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT code_id FROM Skaner WHERE code_id = ?
        ''', (code_id,))
        skaner_result = cursor.fetchone()
        
        if not skaner_result:
            conn.close()
            return "Siz xato code yubordingiz" 
        
        cursor.execute('''
            SELECT code_id FROM tolov WHERE code_id = ?
        ''', (code_id,))
        tolov_result = cursor.fetchone()
        
        if tolov_result:
            conn.close()
            return "Allaqachon tolov jadvalida mavjud."  
        
        cursor.execute('''
            INSERT INTO tolov (telegram_id, code_id)
            VALUES (?, ?)
        ''', (telegram_id, code_id))

        conn.commit()
        conn.close()
        return f"tolov muvaffaqiyatli amalga oshirildi"

    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        return False




def add_tolov(telegram_id: int, code_id: int) -> bool:
    """Tolov jadvaliga yangi ma'lumot qo'shish funksiyasi"""
    try:
        
        conn = sqlite3.connect('apteka.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tolov (telegram_id, code_id)
            VALUES (?, ?)
        ''', (telegram_id, code_id))
        
        conn.commit()
        conn.close()
        return True 

    except sqlite3.IntegrityError:
        print("Code_id allaqachon mavjud.")
        return False 
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        return False




def add_code(code_id: int) -> bool:
    """Skaner jadvaliga yangi code_id qo'shish funksiyasi"""
    try:
        conn = sqlite3.connect('apteka.db')
        cursor = conn.cursor()
        
      
        cursor.execute('''
            INSERT INTO Skaner (code_id)
            VALUES (?)
        ''', (code_id,))
        
      
        conn.commit()
        conn.close()
        return True 

    except sqlite3.IntegrityError:
        return False 
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        return False






def add_user(name: str, contact: str, telegram_id: int) -> bool:
    try:
        conn = sqlite3.connect('apteka.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, contact, telegram_id)
            VALUES (?, ?, ?)
        ''', (name, contact, telegram_id))
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        return False

def get_user(telegram_id: int) -> bool:
    conn = sqlite3.connect('apteka.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'name': user[1],
            'contact': user[2],
            'telegram_id': user[3]
        }
    return None



def hisobdagi_summa(telegram_id: int) -> bool:
    conn = sqlite3.connect('apteka.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tolov WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchall()

    if telegram_id:
        a = 0
        for i in user:
            a += 1
        return a
    
    return 0


def tolov_and_delete(telegram_id):
    """Pulni yechib olgandan kegin tolov tabledan malumotlarni o'chirib tashlaydi"""

    try:
        conn = sqlite3.connect('apteka.db')
        cursor = conn.cursor()

        cursor.execute(f'DELETE FROM tolov WHERE telegram_id={telegram_id}')
        conn.commit()
        conn.close()

        return True
    
    except Exception as e:
        print(f'Xatolik yuz berdi {e}')
        return False