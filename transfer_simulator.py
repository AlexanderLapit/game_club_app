import subprocess
import os
import json
from datetime import datetime

def run_transfer_simulator(data):
    """
    Эмулирует передачу данных через TransferSimulator.exe
    """
    # Сохраняем данные во временный файл
    temp_file = "temp_transfer_data.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    try:
        # Запускаем .exe (если есть)
        if os.path.exists("TransferSimulator.exe"):
            result = subprocess.run(
                ["TransferSimulator.exe", temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            success = result.returncode == 0
        else:
            # Режим эмуляции
            print(f"[Эмуляция] Передача данных из {temp_file}...")
            success = True  # Имитация успешной передачи

    except Exception as e:
        print(f"Ошибка при запуске TransferSimulator.exe: {e}")
        success = False
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return success