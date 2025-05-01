from pydantic import BaseModel


class VacancyType(BaseModel):
    title: str
    company: str
    salary: str