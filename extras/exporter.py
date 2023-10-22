import json
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import Sequence, Type


class FileFormat(str, Enum):
    DOCUMENT = "docx"
    EXCEL = "xlsx"
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"


@dataclass(order=True)
class ExportData:
    headers: Sequence
    rows: Sequence
    metadata: dict | None


class AbstractExporter(ABC):
    def load_data(self, data: ExportData):
        ...

    def export(self) -> bytes:
        ...


class JSONExporter(AbstractExporter):
    def load_data(self, data: ExportData):
        self.data = data

    def export(self) -> bytes:
        buffer = BytesIO()
        if self.data:
            json.dump(self.data.metadata, buffer)
            return buffer.read()


def get_exporter_class(format: FileFormat) -> Type[AbstractExporter]:
    return {FileFormat.JSON: JSONExporter}[format]


def get_media_type(format: FileFormat) -> str:
    return {
        FileFormat.DOCUMENT: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        FileFormat.EXCEL: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        FileFormat.PDF: "application/pdf",
        FileFormat.CSV: "text/csv",
        FileFormat.JSON: "text/json",
    }[format]
