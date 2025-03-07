.. _errors:

Errors
======

.. currentmodule:: fastapi_jsonapi

The JSON:API 1.0 specification recommends to return errors like this:

.. sourcecode:: http

    HTTP/1.1 422 Unprocessable Entity
    Content-Type: application/vnd.api+json

    {
      "errors": [
        {
          "status": "422",
          "source": {
            "pointer":"/data/attributes/first-name"
          },
          "title":  "Invalid Attribute",
          "detail": "First name must contain at least three characters."
        }
      ],
      "jsonapi": {
        "version": "1.0"
      }
    }

The "source" field gives information about the error if it is located in data provided or in a query string parameter.

The previous example shows an error located in data provided. The following example shows error in the query string parameter "include":

.. sourcecode:: http

    HTTP/1.1 400 Bad Request
    Content-Type: application/vnd.api+json

    {
      "errors": [
        {
          "status": "400",
          "source": {
            "parameter": "include"
          },
          "title":  "BadRequest",
          "detail": "Include parameter is invalid"
        }
      ],
      "jsonapi": {
        "version": "1.0"
      }
    }

fastapi-jsonapi-next provides two kinds of helpers for displaying errors:


| * **the exceptions module**: you can import a lot of exceptions from this `module <https://github.com/eljefedelrodeodeljefe/fastapi-jsonapi-next/blob/main/fastapi_jsonapi/exceptions/json_api.py>`_ that helps you to raise exceptions that will be well-formatted according to the JSON:API 1.0 specification

When you create custom code for your API I recommend using exceptions from the fastapi-jsonapi-next's exceptions module to raise errors because HTTPException-based exceptions are caught and rendered according to the JSON:API 1.0 specification.


You can raise an exception in any point yor app. ResourceManager, DataLayer, etc.
All of the exceptions defined by fastapi-jsonapi-next will handled by the root handler
``fastapi_jsonapi.exceptions.handlers.base_exception_handler`` and we'll see pretty JSON:API spec output

Example:

.. code-block:: python

    from fastapi_jsonapi.exceptions import BadRequest
    from fastapi_jsonapi.schema import BaseJSONAPIDataInSchema, JSONAPIResultDetailSchema
    from fastapi_jsonapi.views.list_view import ListViewBase


    class CustomErrorView(ListViewBase):
        def post_resource_list_result(
            self,
            data_create: BaseJSONAPIDataInSchema,
            **extra_view_deps,
        ) -> JSONAPIResultDetailSchema:
            try:
                # any logic here
                pass
            except Exception:
                raise BadRequest(detail="My custom err")

Request:

.. literalinclude:: ./http_snippets/snippets/errors__create_user
  :language: http

Response:

.. literalinclude:: ./http_snippets/snippets/errors__create_user_result
  :language: http
