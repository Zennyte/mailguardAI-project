from pydantic import BaseModel, EmailStr, Field


# Forma e regjistrimit (faqja Register)
class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


# Forma e kycjes (faqja Login)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Perdoruesi i kycur (pa fjalekalim), me rolet dhe lejet e tij.
# Tokenat nuk ndodhen ketu - ato dergohen vetem si cookie "httpOnly".
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool
    roles: list[str] = []
    permissions: list[str] = []
