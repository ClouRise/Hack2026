import uuid
import requests 
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import threading
import urllib3
import time, json
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GigaChatClient:
    def __init__(self, credentials: Optional[str] = None, base_url: Optional[str] = None):
        """
        Инициализация клиента GigaChat API
        
        Args:
            credentials (str, optional): Ключ авторизации в формате Base64
            base_url (str, optional): Базовый URL API
        """
        # Загрузка данных из environment variables
        self.credentials = "MDE5ZDBjZjctMDc3Yi03ZDNhLWFmMTEtYTljMWNlZGE0ODQ3OmViNTdhYzMzLWYyNTctNDVmNi04MzdjLTYwMjlkZmJjMDA5YQ=="
        self.base_url = base_url or os.getenv('GIGACHAT_BASE_URL', "https://gigachat.devices.sberbank.ru/api/v1")
        self.client_id = "019d0cf7-077b-7d3a-af11-a9c1ceda4847"
        self.client_secret = "eb57ac33-f257-45f6-837c-6029dfbc009a"
        self.scope = os.getenv('GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
        
        if not self.credentials and (self.client_id and self.client_secret):
            # Генерируем credentials из client_id и client_secret
            import base64
            auth_string = f"{self.client_id}:{self.client_secret}"
            self.credentials = base64.b64encode(auth_string.encode()).decode()
        
        if not self.credentials:
            raise ValueError("Не указаны credentials для авторизации. Укажите GIGACHAT_CREDENTIALS или GIGACHAT_CLIENT_ID и GIGACHAT_CLIENT_SECRET в .env файле")
        
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        self.token_refresh_thread = None
        self.stop_refresh = threading.Event()
        
        # Получаем первоначальный токен
        self.get_token()
        
        # Запускаем поток для обновления токена
        self._start_token_refresh()
    
    def _generate_rquid(self) -> str:
        """Генерация уникального идентификатора запроса"""
        return str(uuid.uuid4())
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Получить заголовки для запроса
        
        Returns:
            Dict[str, str]: Заголовки запроса
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        else:
            # Используем базовую аутентификацию
            headers['Authorization'] = f'Basic {self.credentials}'
        return headers
    
    def get_token(self) -> Optional[Dict]:
        """
        Получить токен доступа
        
        Returns:
            Optional[Dict]: Ответ с токеном доступа
        """
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f'Basic {self.credentials}',
            'RqUID': self._generate_rquid()
        }
        data = {
            'scope': self.scope
        }
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                data=data,
                verify=False,
                timeout=30
            )
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            
            # Вычисляем время истечения токена (30 минут - 5 минут для запаса)
            expires_in = token_data.get('expires_in', 1800)  # 30 минут по умолчанию
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
            
            print(f"Токен получен. Истекает в: {self.token_expires_at}")
            return token_data
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении токена: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Статус код: {e.response.status_code}")
                print(f"Текст ответа: {e.response.text}")
            return None
    
    def refresh_access_token(self) -> bool:
        """
        Обновить access token с помощью refresh token
        
        Returns:
            bool: Успешно ли обновлен токен
        """
        if not self.refresh_token:
            print("Refresh token отсутствует, получаем новый токен")
            return self.get_token() is not None
        
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f'Basic {self.credentials}',
            'RqUID': self._generate_rquid()
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                data=data,
                verify=False,
                timeout=30
            )
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            
            # Обновляем время истечения
            expires_in = token_data.get('expires_in', 1800)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
            
            print(f"Токен обновлен. Новое время истечения: {self.token_expires_at}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обновлении токена: {e}")
            # Если refresh token невалиден, получаем новый токен
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 400:
                    print("Refresh token невалиден, получаем новый токен")
                    return self.get_token() is not None
            return False
    
    def _token_refresh_worker(self):
        """Рабочий поток для автоматического обновления токена"""
        while not self.stop_refresh.is_set():
            try:
                # Проверяем, нужно ли обновить токен
                if self.token_expires_at and datetime.now() >= self.token_expires_at:
                    print("Токен истек, обновляем...")
                    self.refresh_access_token()
                elif self.token_expires_at:
                    # Вычисляем время до обновления (25 минут)
                    time_to_refresh = (self.token_expires_at - datetime.now()).total_seconds() - 300  # 5 минут запаса
                    if time_to_refresh > 0:
                        # Ждем до времени обновления или остановки потока
                        self.stop_refresh.wait(time_to_refresh)
                    else:
                        # Немедленное обновление
                        self.refresh_access_token()
                else:
                    # Если время истечения не установлено, ждем 1 минуту
                    self.stop_refresh.wait(60)
                    
            except Exception as e:
                print(f"Ошибка в потоке обновления токена: {e}")
                time.sleep(60)  # Ждем перед повторной попыткой
    
    def _start_token_refresh(self):
        """Запуск потока для автоматического обновления токена"""
        if self.token_refresh_thread is None or not self.token_refresh_thread.is_alive():
            self.stop_refresh.clear()
            self.token_refresh_thread = threading.Thread(target=self._token_refresh_worker, daemon=True)
            self.token_refresh_thread.start()
            print("Поток обновления токена запущен")
    
    def stop_token_refresh(self):
        """Остановка потока обновления токена"""
        self.stop_refresh.set()
        if self.token_refresh_thread and self.token_refresh_thread.is_alive():
            self.token_refresh_thread.join(timeout=5)
        print("Поток обновления токена остановлен")
    
    def chat(self, request_data: Dict) -> Optional[Dict]:
        """
        Базовый метод для отправки запроса к /chat/completions
        
        Args:
            request_data (Dict): Данные для запроса
            
        Returns:
            Optional[Dict]: Ответ от API
        """
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=request_data,
                verify=False,  # Отключаем проверку SSL для тестирования
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Статус код: {e.response.status_code}")
                print(f"Текст ответа: {e.response.text}")
            return None
    
    def chat_with_system_message(self, system_message: str, user_message: str, 
                               model: str = "GigaChat", **kwargs) -> Optional[Dict]:
        """
        Получить ответ от модели с системным сообщением и пользовательским сообщением
        
        Args:
            system_message (str): Системное сообщение, задающее роль модели
            user_message (str): Пользовательское сообщение
            model (str): Модель для генерации (по умолчанию "GigaChat")
            **kwargs: Дополнительные параметры для запроса
            
        Returns:
            Optional[Dict]: Ответ от модели
        """
        messages = [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user", 
                "content": user_message
            }
        ]
        
        # Базовые параметры запроса
        request_data = {
            "model": model,
            "messages": messages,
            "stream": False,
            "temperature": 0
        }
        
        # Обновляем параметры из kwargs
        request_data.update(kwargs)
        
        return self.chat(request_data)
    
    def chat_with_messages(self, messages: List[Dict], model: str = "GigaChat", 
                          **kwargs) -> Optional[Dict]:
        """
        Получить ответ от модели с произвольным списком сообщений
        
        Args:
            messages (List[Dict]): Список сообщений в формате [{"role": "...", "content": "..."}]
            model (str): Модель для генерации
            **kwargs: Дополнительные параметры для запроса
            
        Returns:
            Optional[Dict]: Ответ от модели
        """
        request_data = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        request_data.update(kwargs)
        return self.chat(request_data)
    
    def chat_stream(self, request_data: Dict):
        """
        Метод для потокового получения ответа
        
        Args:
            request_data (Dict): Данные для запроса
            
        Yields:
            Dict: Части ответа от модели
        """
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()
        
        # Убедимся, что stream=True
        request_data['stream'] = True
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=request_data,
                stream=True,
                verify=False,  # Отключаем проверку SSL для тестирования
                timeout=30
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # Убираем 'data: '
                        if data == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            yield chunk
                        except json.JSONDecodeError:
                            continue
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении потокового запроса: {e}")
    
    def get_models(self) -> Optional[Dict]:
        """
        Получить список доступных моделей
        
        Returns:
            Optional[Dict]: Список моделей
        """
        url = f"{self.base_url}/models"
        headers = self._get_headers()
        
        try:
            response = requests.get(
                url=url,
                headers=headers,
                verify=False,  # Отключаем проверку SSL для тестирования
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении списка моделей: {e}")
            return None

    def __del__(self):
        """Деструктор - останавливаем поток при удалении объекта"""
        self.stop_token_refresh()


# Создание глобального синглтон объекта
class GigaChatSingleton:
    """
    Singleton обертка для GigaChatClient
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = GigaChatClient()
            return cls._instance
    
    def __getattr__(self, name):
        return getattr(self._instance, name)
    
    def __setattr__(self, name, value):
        if name == '_instance':
            super().__setattr__(name, value)
        else:
            setattr(self._instance, name, value)

gigachat = GigaChatSingleton()