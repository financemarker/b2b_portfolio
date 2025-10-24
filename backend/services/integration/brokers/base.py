from abc import ABC, abstractmethod
from typing import Any, List

class BrokerBase(ABC):
    """
    Базовый интерфейс брокера: определяет набор обязательных методов,
    а также утилиты, общие для всех интеграций.
    """

    broker_code: str                # уникальный идентификатор брокера (например 'tinkoff')
    strategy: str                   # тип подключения ('api', 'file', 'oauth2', и т.п.)

    def __init__(self, **kwargs):
        """Опциональные параметры для конфигурации брокера"""
        for k, v in kwargs.items():
            setattr(self, k, v)

    # === обязательные методы ===
    @abstractmethod
    async def create_connections(self, **kwargs) -> list[dict]:
        """Создание новых connections (через токен, логин и т.п.)"""
        pass

    @abstractmethod
    async def import_operations(self, **kwargs) -> list[dict]:
        """Импорт сделок / операций"""
        pass


    def __repr__(self):
        return f"<Broker {self.broker_code}:{self.strategy}>"
