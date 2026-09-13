from fastapi import HTTPException
from datetime import date

class NabronirovalException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(NabronirovalException):
    detail = 'Объект не найден'

class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Похожий объект уже существует"

class AllRoomsAreBookedException(NabronirovalException):
    detail = 'Не осталось свободных номеров'

def check_date_accuracy(date_from: date, date_to: date):
    if date_to >= date_from:
        raise HTTPException(status_code=422, detail='Дата заезда не может быть позже даты выезда')
    
class NabronivalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsHTTPException(NabronivalHTTPException):
    status_code = 409
    detail = 'Такой пользователь уже существует'


class HotelNotFoundHTTPException(NabronivalHTTPException):
    status_code = 404
    detail = 'Отель не найден'

class RoomNotFoundHTTPException(NabronivalHTTPException):
    status_code = 404
    detail = 'Номер не найден'