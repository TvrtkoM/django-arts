from django.template.defaultfilters import slugify
import datetime

def date_based_slugify(instance, char_field_name, date_field_name, 
                       slug_field_name='slug', date=datetime.date.today()):
    slug = slugify(getattr(instance, char_field_name))
    query_dict = { '{0}__year'.format(date_field_name): date.year,
                   '{0}__month'.format(date_field_name): date.month,
                   '{0}__day'.format(date_field_name): date.day,
                   '{0}__startswith'.format(slug_field_name): slug }
    objs = instance.__class__._default_manager.order_by(slug_field_name).\
                    filter(**query_dict)
    if not objs or getattr(objs[0], slug_field_name) != slug:
        return slug
    format_str = '{0}-{1}'
    if objs[1:]:
        import re
        objs = objs[1:]
        pattern = r'^(?P<slug>[-\w]+)-(?P<num>\d+)?$'
        for i, obj in enumerate(objs):
            match_obj = re.match(pattern, getattr(obj, slug_field_name))
            if match_obj:
                id = int(match_obj.group('num'))
                if i != id:
                    return format_str.format(slug, i)
                else:
                    next_id = i+1
        return format_str.format(slug, next_id)
    else:
        return format_str.format(slug, 0)
