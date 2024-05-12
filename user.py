import requests
import json

class User:
    @staticmethod
    async def register_by_number(phone_number: str, chat_id: str):
        try:
            url = f"https://localhost:44305/api/User/byPhone/{phone_number}?chatId={chat_id}"
            response = requests.get(url, verify=False)
            response = response.json()
            if response["status_code"] == 404:
                return "Вы не имеете доступа"
            if response["status_code"] == 200:
                return "Вы уже подписаны"
            return "Вы успешно зарегистрированы"
        except Exception as err:
            return "Что-то пошло не так, пока"


    
