from pydantic import BaseModel


class SignupPreLaunchRequestDto(BaseModel):
    email: str

class SignupPreLaunchResponseDto(BaseModel):
    success: bool
    message: str
