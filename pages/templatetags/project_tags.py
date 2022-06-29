from django import template

from pages.models import Project

register = template.Library()


@register.simple_tag(takes_context=False)
def get_project_info(project_identity):
    prj = Project.objects.get(identity=project_identity)
    return prj