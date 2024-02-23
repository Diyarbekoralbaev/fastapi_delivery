from pydantic import BaseModel
from typing import Optional

class Signupmodel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'username',
                'email': 'email@gmail.com',
                'password': 'password',
                'is_staff': False,
                'is_active': True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = '8661f1af196b1ae92fd7e0df21828883d8a3307d869cfa4e1de295d9049ae8f9'


class Loginmodel(BaseModel):
    username: str
    password: str
