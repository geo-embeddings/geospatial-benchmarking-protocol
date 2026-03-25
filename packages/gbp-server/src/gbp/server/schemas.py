import datetime as dt
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DatasetCreate(BaseModel):
    title: str
    tags: list[str] = []
    stac_id: str | None = None
    geometry: dict | None = None
    bbox: list[float] | None = None
    datetime: dt.datetime | None = None
    start_datetime: dt.datetime | None = None
    end_datetime: dt.datetime | None = None
    links: list[dict] = []
    assets: dict = {}


class DatasetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    tags: list[str]
    stac_version: str
    stac_id: str | None
    geometry: dict | None
    bbox: list[float] | None
    datetime: dt.datetime | None
    start_datetime: dt.datetime | None
    end_datetime: dt.datetime | None
    links: list[dict]
    assets: dict


class EncoderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class DecoderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class PipelineCreate(BaseModel):
    encoder_id: UUID
    decoder_id: UUID


class PipelineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    encoder_id: UUID
    decoder_id: UUID


class PretrainedModelCreate(BaseModel):
    pretraining_bands: str
    preferred_satellite_source: str
    input_shape: str
    output_shape: str
    pretrained_weight_source: str
    pretraining_data_provenance: str


class PretrainedModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    pretraining_bands: str
    preferred_satellite_source: str
    input_shape: str
    output_shape: str
    pretrained_weight_source: str
    pretraining_data_provenance: str


class ResultCreate(BaseModel):
    dataset_id: UUID
    pretrained_model_id: UUID
    runner_id: UUID


class ResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dataset_id: UUID
    pretrained_model_id: UUID
    runner_id: UUID


class RunnerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
