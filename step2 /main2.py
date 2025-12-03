
#!/usr/bin/env python3
"""
Эмулятор командной строки UNIX - Вариант 7
Этап 2: Конфигурация
"""

import os
import sys
import argparse
import json
from datetime import datetime

# ========== Парсер командной строки ==========
def parse_arguments():
    """Разбор параметров командной строки"""
    parser = argparse.ArgumentParser(
        description='Эмулятор командной строки UNIX',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  %(prog)s                            # Запуск с параметрами по умолчанию
  %(prog)s --vfs-path "./my_vfs"      # Указание пути к VFS
  %(prog)s --start-script init.sh     # Запуск со стартовым скриптом
  %(prog)s --config config.yaml       # Использование конфигурационного файла
        '''
    )
    
    parser.add_argument(
        '--vfs-path',
        help='Путь к физическому расположению VFS',
        default=None
    )
    
    parser.add_argument(
        '--log-file',
        help='Путь к лог-файлу (формат JSON)',
        default='./emulator.log'
    )
    
    parser.add_argument(
        '--start-script',
        help='Путь к стартовому скрипту',
        default=None
    )
    
    parser.add_argument(
        '--config',
        help='Путь к конфигурационному файлу YAML',
        default='./config.yaml'
    )
    
    return parser.parse_args()

# ========== Работа с YAML конфигурацией ==========
def load_yaml_config(config_path):
    """Загрузка конфигурации из YAML файла"""
    config = {}
    
    try:
        import yaml
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
    except ImportError:
        print("⚠️  Внимание: библиотека PyYAML не установлена.")
        print("   Установите: pip3 install pyyaml")
        print("   Будут использованы значения по умолчанию.")
    except yaml.YAMLError as e:
        print(f"❌ Ошибка в формате YAML файла {config_path}: {e}")
    except Exception as e:
        print(f"❌ Ошибка чтения конфигурационного файла {config_path}: {e}")
    
    return config

# ========== Логирование ==========
class Logger:
    """Класс для логирования событий в JSON формате"""
    
    def __init__(self, log_file):
        self.log_file = log_file
        self.setup_log_file()
    
    def setup_log_file(self):
        """Создание лог-файла если его нет"""
        try:
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.write('[]')
        except Exception as e:
            print(f"⚠️  Не удалось создать лог-файл: {e}")
    
    def log_event(self, event_type, command=None, args=None, error=None):
        """Логирование события"""
        try:
            # Читаем существующие логи
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
            
            # Создаем новую запись
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": event_type,
                "user": os.getenv('USER', 'unknown'),
                "hostname": os.uname().nodename.split('.')[0]
            }
            
            if command:
                log_entry["command"] = command
            if args:
                log_entry["args"] = args
            if error:
                log_entry["error"] = str(error)
            
            # Добавляем новую запись
            logs.append(log_entry)
            
            # Сохраняем (ограничиваем размер до 1000 записей)
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️  Ошибка логирования: {e}")

# ========== Стартовый скрипт ==========
def run_start_script(script_path, execute_command_func, logger):
    """Выполнение стартового скрипта"""
    if not script_path or not os.path.exists(script_path):
        return
    
    print(f"\n📜 Выполнение стартового скрипта: {script_path}")
    print("=" * 50)
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            print(f"[{line_num}] $ {line}")
            
            try:
                # Имитируем выполнение команды
                command = line.split()[0] if line.split() else ""
                args = line.split()[1:] if len(line.split()) > 1 else []
                
                if command:
                    execute_command_func(command, args)
                    logger.log_event("script_command", command, args)
                    
            except Exception as e:
                print(f"  ❌ Ошибка: {e}")
                logger.log_event("script_error", command, args, e)
                # Пропускаем ошибочные строки и продолжаем
    
    except Exception as e:
        print(f"❌ Ошибка выполнения стартового скрипта: {e}")
        logger.log_event("script_load_error", error=e)
    
    print("=" * 50)

# ========== Основные функции ==========
def get_prompt(vfs_name="default"):
    """Формирует приглашение с именем VFS"""
    username = os.getenv('USER', 'user')
    hostname = os.uname().nodename.split('.')[0]
    return f"{username}@{hostname}:{vfs_name}$ "

def simple_parse_input(user_input):
    """Простой парсер команд"""
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]

def execute_command(command, args, logger):
    """Выполняет команду с логированием"""
    logger.log_event("command_exec", command, args)
    
    if command == "1s":
        print(f"📁 Команда: {command}")
        print(f"   Аргументы: {args}")
        print("   (реализация будет в этапе 4)")
        
    elif command == "cd":
        print(f"📂 Команда: {command}")
        print(f"   Аргументы: {args}")
        print("   (реализация будет в этапе 4)")
        
    elif command == "conf-dump":
        print("⚙️  Текущая конфигурация:")
        print(f"   VFS Path: {config['vfs_path']}")
        print(f"   Log File: {config['log_file']}")
        print(f"   Start Script: {config['start_script']}")
        print(f"   Config File: {config['config_file']}")
        
    elif command == "help":
        print("📋 Доступные команды:")
        print("   1s [args]     - список файлов")
        print("   cd [dir]      - смена директории")
        print("   conf-dump     - показать конфигурацию")
        print("   exit          - выход из эмулятора")
        print("   help          - эта справка")
        
    elif command == "exit":
        logger.log_event("exit")
        return True  # сигнал для выхода
        
    else:
        print(f"❌ Ошибка: неизвестная команда '{command}'")
        logger.log_event("unknown_command", command, args)
        
    return False

def merge_configurations(cmd_args, file_config):
    """Объединение конфигураций с приоритетом командной строки"""
    config = {
        'vfs_path': './vfs',
        'log_file': './emulator.log',
        'start_script': None,
        'config_file': './config.yaml'
    }
    
    # Сначала значения из файла
    config.update(file_config)
    
    # Затем перезаписываем значениями из командной строки (если указаны)
    if cmd_args.vfs_path is not None:
        config['vfs_path'] = cmd_args.vfs_path
    if cmd_args.log_file:
        config['log_file'] = cmd_args.log_file
    if cmd_args.start_script is not None:
        config['start_script'] = cmd_args.start_script
    if cmd_args.config:
        config['config_file'] = cmd_args.config
    
    return config

# ========== Главная функция ==========
def main():
    print("🚀 Эмулятор командной строки UNIX - Этап 2")
    print("==========================================")
    
    # 1. Парсим аргументы командной строки
    args = parse_arguments()
    
    # 2. Загружаем конфигурацию из YAML файла
    yaml_config = load_yaml_config(args.config)
    
    # 3. Объединяем конфигурации (приоритет у командной строки)
    global config
    config = merge_configurations(args, yaml_config)
    
    # 4. Настраиваем логирование
    logger = Logger(config['log_file'])
    logger.log_event("startup")
    
    # 5. Показываем отладочную информацию
    print("\n⚙️  Конфигурация эмулятора:")
    print("-" * 30)
    for key, value in config.items():
        print(f"  {key:15}: {value or 'не указан'}")
    print("-" * 30)
    
    # 6. Выполняем стартовый скрипт если есть
    if config['start_script']:
        # Функция-заглушка для выполнения команд из скрипта
        def script_command_executor(cmd, cmd_args):
            execute_command(cmd, cmd_args, logger)
        
        run_start_script(config['start_script'], script_command_executor, logger)
    
    # 7. Основной цикл REPL
    print("\n💻 Режим ввода команд (введите 'help' для справки)")
    print("=" * 50)
    
    vfs_name = os.path.basename(config['vfs_path']) if config['vfs_path'] else "default"
    
    while True:
        try:
            # Показываем приглашение
            prompt = get_prompt(vfs_name)
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            # Разбираем команду
            command, cmd_args = simple_parse_input(user_input)
            
            if not command:
                continue
            
            # Выполняем команду
            should_exit = execute_command(command, cmd_args, logger)
            
            if should_exit:
                print("👋 Завершение работы эмулятора...")
                break
                
        except KeyboardInterrupt:
            print("\n⚠️  Для выхода введите 'exit'")
        except EOFError:
            print("\n👋 Завершение работы...")
            break
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            logger.log_event("unexpected_error", error=e)

if __name__ == "__main__":
    main()
EOF
