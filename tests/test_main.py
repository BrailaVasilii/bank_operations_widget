from unittest.mock import patch
from src.main import main


def test_main_with_mocked_functions() -> None:
    with patch("src.main.analyze_cashback_categories") as mocked_cashback:
        mocked_cashback.return_value = {"Еда": 15.0, "Транспорт": 10.0}
        with patch("src.main.get_currency_rate") as mocked_rates:
            mocked_rates.return_value = {"EUR": 0.85, "RUB": 73.0}

            result = main()  # Запускаем функцию main
            assert result["cashback"] == {"Еда": 15.0, "Транспорт": 10.0}  # Проверяем кешбэк
            assert result["currency_rates"] == {"EUR": 0.85, "RUB": 73.0}  # Проверяем курсы валют
