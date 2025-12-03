"""
Парсер командной строки с поддержкой переменных окружения
"""

import os
import re

def expand_environment_vars(text):
    """Раскрывает переменные окружения типа $HOME"""
    def replace_var(match):
        var_name = match.group(1)
        return os.getenv(var_name, '')
    
    return re.sub(r'\$(\w+)', replace_var, text)

def parse_input(user_input):
    """
    Разбирает ввод пользователя
    Возвращает: (команда, список_аргументов)
    """
    # Раскрыть переменные окружения
    expanded = expand_environment_vars(user_input)
    
    # Разделить на части (простой парсер)
    parts = expanded.strip().split()
    
    if not parts:
        return None, []
    
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    
    return command, args
