from pydantic import BaseModel


class VacancyType(BaseModel):
    title: str
    company: str
    salary: str
    required_work_experience: str
    work_format: str
    link: str
    # hard_skills: str