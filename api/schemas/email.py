from pydantic import EmailStr, BaseModel


class EmailGet(BaseModel):
    email_id: int
    email: str

    class Config:
        from_attributes = True


class EmailCreate(BaseModel):
    email: EmailStr
