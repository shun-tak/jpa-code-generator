import re
import shutil
import tempfile


def camel_case(snake_case):
    words = snake_case.split('_')
    first = words[0]
    return first + ''.join((w.capitalize() for w in words[1:]))


def pascal_case(snake_case):
    words = snake_case.split('_')
    return ''.join((w.capitalize() for w in words))


def sed_inplace(filepath, pattern, replace):
    """
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.

    See http://stackoverflow.com/a/31499114
    """

    pattern_compiled = re.compile(pattern)

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filepath) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(replace, line))

    shutil.copystat(filepath, tmp_file.name)
    shutil.move(tmp_file.name, filepath)
