from collections.abc import Iterable, Mapping
from typing import Literal, Optional, Union

import pytest
from pydantic import BaseModel

from datachain.lib.convert.python_to_sql import python_to_sql
from datachain.sql.types import JSON, Array, String


class MyModel(BaseModel):
    val1: str


class MyFeature(BaseModel):
    val1: str


@pytest.mark.parametrize(
    "typ,expected",
    (
        (str, String),
        (String, String),
        (Literal["text"], String),
        (dict[str, int], JSON),
        (Mapping[str, int], JSON),
        (Optional[str], String),
        (Union[dict, list[dict]], JSON),
    ),
)
def test_convert_type_to_datachain(typ, expected):
    assert python_to_sql(typ) == expected


@pytest.mark.parametrize(
    "typ,expected",
    (
        (list[str], Array(String())),
        (Iterable[str], Array(String())),
        (list[list[str]], Array(Array(String()))),
    ),
)
def test_convert_type_to_datachain_array(typ, expected):
    assert python_to_sql(typ).to_dict() == expected.to_dict()


@pytest.mark.parametrize(
    "typ",
    (
        Union[str, int],
        list[Union[str, int]],
        MyFeature,
        MyModel,
    ),
)
def test_convert_type_to_datachain_error(typ):
    with pytest.raises(TypeError):
        python_to_sql(typ)
