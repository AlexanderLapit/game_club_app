from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost:5432/game_club")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE products ADD COLUMN IF NOT EXISTS unit VARCHAR(20) DEFAULT 'шт.';
    """))
    conn.commit()
    print("✅ Колонка 'unit' добавлена в таблицу 'products'")

    # Обновим существующие строки, если unit NULL
    conn.execute(text("""
        UPDATE products SET unit = 'шт.' WHERE unit IS NULL;
    """))
    conn.commit()

    # Сделаем NOT NULL (если нужно)
    try:
        conn.execute(text("""
            ALTER TABLE products ALTER COLUMN unit SET NOT NULL;
        """))
        conn.commit()
        print("✅ Колонка 'unit' теперь NOT NULL")
    except Exception as e:
        print("⚠️ Возможно, уже установлено:", str(e))