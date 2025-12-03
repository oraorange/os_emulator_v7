"""
Реализация команд эмулятора
"""

import os
import sys

def execute_command(command, args):
    """Выполняет команду или заглушку"""
    
    # Команды-заглушки
    if command == "1s":
        print(f"Команда: {command}")
        print(f"Аргументы: {args}")
        # Это заглушка - позже заменим на реальную логику
        
    elif command == "cd":
        print(f"Команда: {command}")
        print(f"Аргументы: {args}")
        # Заглушка
        
    elif command == "help":
        show_help()
        
    else:
        print(f"Ошибка: неизвестная команда '{command}'")
        print("Доступные команды: 1s, cd, exit, help")

def exit_shell():
    """Завершает работу эмулятора"""
    print("Завершение работы эмулятора...")
    sys.exit(0)

def show_help():
    """Показывает справку по командам"""
    print("Доступные команды:")
    print("  1s [args]     - список файлов (заглушка)")
    print("  cd [dir]      - смена директории (заглушка)")
    print("  exit          - выход из эмулятора")
    print("  help          - эта справка")
