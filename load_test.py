#!/usr/bin/env python3
"""
Сценарій для автоматичного генерування навантаження на REST сервіс
Емулятор генерації запитів до веб сайту

Використання:
    python load_test.py --url http://localhost:8000 --users 10 --duration 60
    python load_test.py --url https://your-app.awsapprunner.com --users 50 --duration 300
"""

import argparse
import asyncio
import aiohttp
import time
import random
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional
from statistics import mean, median, stdev


class LoadTestStats:
    """Клас для зберігання статистики навантаження"""
    
    def __init__(self):
        self.requests = []
        self.errors = []
        self.start_time = None
        self.end_time = None
        
    def add_request(self, method: str, endpoint: str, status: int, duration: float, error: Optional[str] = None):
        """Додати запит до статистики"""
        self.requests.append({
            'method': method,
            'endpoint': endpoint,
            'status': status,
            'duration': duration,
            'timestamp': time.time(),
            'error': error
        })
        if error or status >= 400:
            self.errors.append({
                'method': method,
                'endpoint': endpoint,
                'status': status,
                'error': error,
                'timestamp': time.time()
            })
    
    def get_stats(self) -> Dict:
        """Отримати статистику"""
        if not self.requests:
            return {}
        
        durations = [r['duration'] for r in self.requests]
        status_codes = [r['status'] for r in self.requests]
        
        total_requests = len(self.requests)
        total_errors = len(self.errors)
        success_rate = ((total_requests - total_errors) / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            'total_requests': total_requests,
            'total_errors': total_errors,
            'success_rate': f"{success_rate:.2f}%",
            'avg_response_time': f"{mean(durations):.3f}s",
            'median_response_time': f"{median(durations):.3f}s",
            'min_response_time': f"{min(durations):.3f}s",
            'max_response_time': f"{max(durations):.3f}s",
            'std_dev': f"{stdev(durations):.3f}s" if len(durations) > 1 else "0.000s",
            'requests_per_second': total_requests / (self.end_time - self.start_time) if self.end_time and self.start_time else 0,
            'status_codes': {code: status_codes.count(code) for code in set(status_codes)},
        }
        
        return stats
    
    def print_stats(self):
        """Вивести статистику"""
        stats = self.get_stats()
        if not stats:
            print("Немає статистики для відображення")
            return
        
        print("\n" + "="*80)
        print("СТАТИСТИКА НАВАНТАЖЕННЯ")
        print("="*80)
        print(f"Загальна кількість запитів: {stats['total_requests']}")
        print(f"Кількість помилок: {stats['total_errors']}")
        print(f"Успішність: {stats['success_rate']}")
        print(f"Запитів в секунду: {stats['requests_per_second']:.2f}")
        print(f"\nЧас відповіді:")
        print(f"  Середній: {stats['avg_response_time']}")
        print(f"  Медіана: {stats['median_response_time']}")
        print(f"  Мінімальний: {stats['min_response_time']}")
        print(f"  Максимальний: {stats['max_response_time']}")
        print(f"  Стандартне відхилення: {stats['std_dev']}")
        print(f"\nКоди статусів:")
        for code, count in sorted(stats['status_codes'].items()):
            print(f"  {code}: {count}")
        print("="*80 + "\n")


class LoadTester:
    """Клас для генерації навантаження"""
    
    def __init__(self, base_url: str, num_users: int, duration: int, ramp_up: int = 10):
        self.base_url = base_url.rstrip('/')
        self.num_users = num_users
        self.duration = duration
        self.ramp_up = ramp_up
        self.stats = LoadTestStats()
        self.running = False
        
        # Endpoints для тестування
        self.endpoints = [
            {'method': 'GET', 'path': '/health', 'weight': 20},
            {'method': 'GET', 'path': '/user/', 'weight': 15},
            {'method': 'GET', 'path': '/authorization/', 'weight': 15},
            {'method': 'GET', 'path': '/label/label_to_creators', 'weight': 15},
            {'method': 'GET', 'path': '/user/download', 'weight': 10},
            {'method': 'GET', 'path': '/docs', 'weight': 10},
            {'method': 'GET', 'path': '/user/1', 'weight': 5},
            {'method': 'GET', 'path': '/authorization/1', 'weight': 5},
            {'method': 'POST', 'path': '/authorization/', 'weight': 3},
            {'method': 'POST', 'path': '/user/', 'weight': 2},
        ]
        
        # Нормалізуємо ваги
        total_weight = sum(e['weight'] for e in self.endpoints)
        for endpoint in self.endpoints:
            endpoint['probability'] = endpoint['weight'] / total_weight
    
    def get_random_endpoint(self) -> Dict:
        """Отримати випадковий endpoint згідно з вагами"""
        rand = random.random()
        cumulative = 0
        for endpoint in self.endpoints:
            cumulative += endpoint['probability']
            if rand <= cumulative:
                return endpoint
        return self.endpoints[0]
    
    def generate_post_data(self, endpoint: str) -> Optional[Dict]:
        """Генерувати дані для POST запитів"""
        if '/authorization/' in endpoint:
            return {
                'email': f'user{random.randint(1000, 9999)}@test.com',
                'password': f'password{random.randint(1000, 9999)}'
            }
        elif '/user/' in endpoint:
            return {
                'name': f'Test User {random.randint(1000, 9999)}',
                'authorization_id': random.randint(1, 100),
                'subscription_id': random.randint(1, 10)
            }
        return None
    
    async def make_request(self, session: aiohttp.ClientSession, endpoint: Dict) -> None:
        """Виконати один запит"""
        method = endpoint['method']
        path = endpoint['path']
        url = f"{self.base_url}{path}"
        
        start_time = time.time()
        status = 0
        error = None
        
        try:
            if method == 'GET':
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    status = response.status
                    await response.read()  # Читаємо відповідь
            elif method == 'POST':
                data = self.generate_post_data(path)
                async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    status = response.status
                    await response.read()
            
            duration = time.time() - start_time
            self.stats.add_request(method, path, status, duration, error)
            
        except asyncio.TimeoutError:
            duration = time.time() - start_time
            error = "Timeout"
            self.stats.add_request(method, path, 0, duration, error)
        except Exception as e:
            duration = time.time() - start_time
            error = str(e)
            self.stats.add_request(method, path, 0, duration, error)
    
    async def user_simulation(self, user_id: int, session: aiohttp.ClientSession) -> None:
        """Симуляція поведінки одного користувача"""
        end_time = time.time() + self.duration
        
        while time.time() < end_time and self.running:
            endpoint = self.get_random_endpoint()
            await self.make_request(session, endpoint)
            
            # Випадкова затримка між запитами (0.1-2 секунди)
            await asyncio.sleep(random.uniform(0.1, 2.0))
    
    async def run_load_test(self) -> None:
        """Запустити тест навантаження"""
        print(f"\n{'='*80}")
        print(f"ПОЧАТОК ТЕСТУ НАВАНТАЖЕННЯ")
        print(f"{'='*80}")
        print(f"URL: {self.base_url}")
        print(f"Кількість користувачів: {self.num_users}")
        print(f"Тривалість: {self.duration} секунд")
        print(f"Ramp-up: {self.ramp_up} секунд")
        print(f"Час початку: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        self.running = True
        self.stats.start_time = time.time()
        
        # Створюємо сесію з налаштуваннями
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=50)
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Ramp-up: поступове збільшення навантаження
            tasks = []
            for i in range(self.num_users):
                task = asyncio.create_task(self.user_simulation(i, session))
                tasks.append(task)
                
                # Поступове додавання користувачів
                if i < self.num_users - 1:
                    await asyncio.sleep(self.ramp_up / self.num_users)
            
            # Чекаємо завершення тесту
            await asyncio.sleep(self.duration)
            
            # Зупиняємо всі задачі
            self.running = False
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self.stats.end_time = time.time()
        
        # Виводимо статистику
        self.stats.print_stats()
        
        # Зберігаємо статистику у файл
        self.save_stats_to_file()
    
    def save_stats_to_file(self) -> None:
        """Зберегти статистику у файл"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'load_test_stats_{timestamp}.json'
        
        stats_data = {
            'test_config': {
                'base_url': self.base_url,
                'num_users': self.num_users,
                'duration': self.duration,
                'ramp_up': self.ramp_up,
            },
            'stats': self.stats.get_stats(),
            'requests': self.stats.requests[:1000],  # Зберігаємо тільки перші 1000 запитів
            'errors': self.stats.errors,
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        print(f"Статистика збережена у файл: {filename}")


async def main():
    """Головна функція"""
    parser = argparse.ArgumentParser(
        description='Сценарій для генерації навантаження на REST сервіс',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  # Локальне тестування
  python load_test.py --url http://localhost:8000 --users 10 --duration 60
  
  # Тестування на AWS
  python load_test.py --url https://your-app.awsapprunner.com --users 50 --duration 300
  
  # Інтенсивне навантаження
  python load_test.py --url https://your-app.awsapprunner.com --users 100 --duration 600 --ramp-up 30
        """
    )
    
    parser.add_argument(
        '--url',
        type=str,
        required=True,
        help='Базовий URL REST сервісу (наприклад: http://localhost:8000 або https://your-app.awsapprunner.com)'
    )
    
    parser.add_argument(
        '--users',
        type=int,
        default=10,
        help='Кількість одночасних користувачів (за замовчуванням: 10)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Тривалість тесту в секундах (за замовчуванням: 60)'
    )
    
    parser.add_argument(
        '--ramp-up',
        type=int,
        default=10,
        help='Час ramp-up в секундах (за замовчуванням: 10)'
    )
    
    args = parser.parse_args()
    
    # Валідація аргументів
    if args.users < 1:
        print("Помилка: кількість користувачів повинна бути більше 0", file=sys.stderr)
        sys.exit(1)
    
    if args.duration < 1:
        print("Помилка: тривалість повинна бути більше 0", file=sys.stderr)
        sys.exit(1)
    
    # Створюємо та запускаємо тестер
    tester = LoadTester(
        base_url=args.url,
        num_users=args.users,
        duration=args.duration,
        ramp_up=args.ramp_up
    )
    
    try:
        await tester.run_load_test()
    except KeyboardInterrupt:
        print("\n\nТест перервано користувачем")
        tester.running = False
        tester.stats.end_time = time.time()
        tester.stats.print_stats()
        sys.exit(0)
    except Exception as e:
        print(f"\n\nПомилка під час виконання тесту: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())

