{% if cookiecutter.include_celery == 'yes' -%}
from {{cookiecutter.repo_name}}.celery import app as celery_app


{% endif -%}

default_app_config = '{{cookiecutter.repo_name}}.apps.{{cookiecutter.repo_name|capitalize}}Config'

{%- if cookiecutter.include_celery == 'yes' %}

__all__ = ['celery_app']
{%- endif %}
