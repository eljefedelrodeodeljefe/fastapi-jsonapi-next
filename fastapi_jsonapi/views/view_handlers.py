import inspect
from functools import partial
from typing import TYPE_CHECKING, Callable, Dict, Optional, Type

from pydantic import BaseModel as PydanticBaseModel

from fastapi_jsonapi.schema_base import BaseModel
from fastapi_jsonapi.views.utils import (
    ALL_METHODS,
    HTTPMethodConfig,
    HTTPMethods,
)

if TYPE_CHECKING:
    from fastapi_jsonapi.views.view_base import ViewBase


async def _run_handler(
    view: "ViewBase",
    handler: Callable,
    dto: Optional[BaseModel] = None,
):
    handler = partial(handler, view, dto) if dto is not None else partial(handler, view)

    if inspect.iscoroutinefunction(handler):
        return await handler()

    return handler()


async def _handle_config(view: "ViewBase", method_config: HTTPMethodConfig, extra_view_deps: Dict) -> Dict:
    if method_config.handler is None:
        return {}

    if method_config.dependencies:
        dto_class: Type[PydanticBaseModel] = method_config.dependencies
        dto = dto_class(**extra_view_deps)
        dl_kwargs = await _run_handler(view, method_config.handler, dto)

        return dl_kwargs

    dl_kwargs = await _run_handler(view, method_config.handler)

    return dl_kwargs


async def handle_endpoint_dependencies(
    view: "ViewBase",
    method: HTTPMethods,
    extra_view_deps: Dict,
) -> Dict:
    """
    :return dict: this is **kwargs for DataLayer.__init___
    """
    dl_kwargs = {}
    if common_method_config := view.method_dependencies.get(ALL_METHODS):
        dl_kwargs.update(await _handle_config(view, common_method_config, extra_view_deps))

    if method_config := view.method_dependencies.get(method):
        dl_kwargs.update(await _handle_config(view, method_config, extra_view_deps))

    return dl_kwargs
