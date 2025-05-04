import logging
import pandas as pd
from pydantic import BaseModel
from base import BaseFileSaver


logger = logging.getLogger(__name__)


class ExcelSaver(BaseFileSaver):
    """
    Сохранение в exel-файл.
    """
    
    _extension = "xlsx"
    
    def _save(self, filepath: str, list_data: list[BaseModel]) -> None:
        """
        Реализация сохранения.

        Args:
            filepath (str): Путь файла для сохранения.
            list_data (list[BaseModel]): Данные для сохранения.
        """
        df = pd.DataFrame([model.dict() for model in list_data])
        df.to_excel(filepath, index=False)