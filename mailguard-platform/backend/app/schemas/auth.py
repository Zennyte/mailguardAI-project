from pydantic import BaseModel, EmailStr, Field


# Te dhenat e kerkuara per regjistrim
class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


# Te dhenat e kerkuara per login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Trupi i kerkeses per /auth/refresh
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Pergjigja me access + refresh token
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Te dhenat e perdoruesit te kthyera nga API (pa fjalekalim)
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool
    roles: list[str] = []

    model_config = {"from_attributes": True}
