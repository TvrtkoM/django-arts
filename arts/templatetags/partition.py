from django import template

register = template.Library()

@register.filter
def partition(thelist, n):
    newlist = [[]]
    for i, elem in enumerate(thelist):
        newlist[-1].append(elem)
        if elem==thelist[len(thelist)-1]:
            break
        elif (i+1)%n == 0:
            newlist.append([])
    return newlist
