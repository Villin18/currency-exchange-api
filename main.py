from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
app = FastAPI(title="Currency Exchange API", description="Получение курсов валют от ЦБ РФ")

load_dotenv()

def get_exchange_rates():
    url = os.environ.get('http_re')

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        usd_rate = data['Valute']['USD']['Value']
        eur_rate = data['Valute']['EUR']['Value']

        return {
            "USD": round(usd_rate, 2),
            "EUR": round(eur_rate, 2),
            "timestamp": data.get('Timestamp', 'N/A')
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при получении данных: {str(e)}")
    except KeyError as e:
        raise Exception(f"Ошибка в структуре данных: {str(e)}")


@app.get("/rates")
async def get_rates():
    try:
        rates = get_exchange_rates()
        return rates
    except Exception as e:
        return {"error": str(e)}


def test_api():
    url = 'http://127.0.0.1:8000/rates'

    try:
        print("Отправка запроса к API...")
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if "error" in data:
            print(f"Ошибка от сервера: {data['error']}")
        else:
            print("Курсы валют получены успешно:")
            print(f"USD: {data['USD']} ₽")
            print(f"EUR: {data['EUR']} ₽")
            print(f"Время обновления: {data['timestamp']}")

    except requests.exceptions.ConnectionError:
        print("Ошибка: Сервер не запущен или недоступен")
    except requests.exceptions.Timeout:
        print("Ошибка: Превышен таймаут запроса")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {str(e)}")
    except KeyError as e:
        print(f"Ошибка в данных ответа: {str(e)}")

if __name__ == "__main__":
        test_api()