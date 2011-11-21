from django import template

register = template.Library()

@register.filter
def shorten(s, maxlen):
    '''return a short version of string s if its longer than maxlen characters.
    '''
    if len(s) <= maxlen:
        return s
    else:
        words = s.split()
        if len(words) is 1:
            return s[:maxlen-4] + u' ...'
        for i in range(1, len(words)):
            s_ = " ".join(words[:-i])
            if len(s_) < maxlen-4:
                break
        return s_ + u' ...'
