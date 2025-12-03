#!/usr/bin/env python3
"""
Эмулятор командной строки UNIX - Вариант 7
"""

import os
import sys
from parser import parse_input
from commands import execute_command, exit_shell

def get_prompt():
    """Формирует приглашение с именем VFS"""
    username = os.getenv('USER', 'user')
    hostname = os.uname().nodename.split('.')[0]
    vfs_name = os.getenv('VFS_NAME', 'default')
    return f"{username}@{hostname}:{vfs_name}$ "

def main():
    print("Эмулятор командной строки UNIX")
    print("Введите 'exit' для выхода")
    print("=" * 50)
    
    while True:
        try:
            # Показать приглашение
            prompt = get_prompt()
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            # Разобрать команду
            command, args = parse_input(user_input)
            
            # Проверить на exit
            if command == "exit":
                exit_shell()
                break
            
            # Выполнить команду
            execute_command(command, args)
            
        except KeyboardInterrupt:
            print("\nДля выхода введите 'exit'")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
