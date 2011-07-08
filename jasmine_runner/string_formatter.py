
def format(errors):
    ret = []
    for error in errors:
        ret.extend(_print(error, [], 0));
    return '\n'.join(ret)


def _print(obj, buffer, level):
    for title, desc in obj.iteritems():
        buffer.append((level * 2 * ' ') + title);
        if desc and isinstance(desc[0], basestring):
            for err in desc:
                buffer.append('%s >> %s' %((level * 2 * ' '), err));
        else:
            level += 1;
            for suite in desc:
                _print(suite, buffer, level);

    return buffer


