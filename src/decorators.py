import logging
import functools
from typing import Optional, Callable, Any


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функции.

    Args:
        filename (Optional[str], optional): Имя файла для записи логов. Если не задано, логи выводятся в консоль.

    Returns:
        Callable: Декорированная функция.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            handler: Optional[logging.Handler] = None
            if filename:
                handler = logging.FileHandler(filename)
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok. Result: {result}")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise
            finally:
                if handler:
                    handler.close()
                    logger.removeHandler(handler)

        return wrapper

    return decorator
