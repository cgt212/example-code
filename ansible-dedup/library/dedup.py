#!/usr/bin/env python

import os
import re
import tempfile
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

def _write_dedup_file(module, lines, message):
    """Write the new file to a temp file and use an atomic_move,
    also create the backup file if it was requested.  The function
    does not return, it will send the result to ansible.

    module: the module object to be used to interact with ansible
    lines: the lines to be written to the file
    message: the message that is sent back to ansible
    """
    backupdest = ""
    if module.params['backup']:
        backupdest = module.backup_local(module.params['dest'])

    tmpfd, tmpfile = tempfile.mkstemp(dir=module.tmpdir)
    with os.fdopen(tmpfd, 'w') as f:
        f.writelines(lines)

    module.atomic_move(tmpfile, to_native(os.path.realpath(module.params['dest'])))

    module.exit_json(changed=True, msg=message, backup=backupdest)

def _global_unique_search(lines):
    """Remove repeated lines so that the entire file is unique.
    Returns the unique lines.

    lines: the lines of the file to deduplicate
    """
    unique_lines = []
    _idx = {}
    for line in lines:
        try:
            _idx[line]
        except KeyError:
            _idx[line] = True
            unique_lines.append(line)
    return unique_lines

def _global_unique_search_i(lines):
    """Remove repeated lines so that the entire file is unique, ignoring
    whitespace.
    Returns the unique lines.

    lines: the lines of the file to deduplicate
    """
    unique_lines = []
    _idx = {}
    for line in lines:
        try:
            _idx[line.strip()]
        except KeyError:
            _idx[line.strip()] = True
            unique_lines.append(line)
    return unique_lines


def _regex_search(regex, lines, first):
    """Remove all except 1 line that matches the regex.
    Returns the unique lines.

    regex: the regular expression to match
    lines: the lines of the file to deduplicate
    first: if the first match should be kept, if false, the last match is kept
    """
    unique_lines = []
    last_match = -1
    for line in lines:
        res = re.match(regex, line)
        if res is not None:
            if last_match < 0:
                unique_lines.append(line)
                last_match = len(unique_lines)-1
            elif last_match >= 0 and not first:
                unique_lines.pop(last_match)
                unique_lines.append(line)
                last_match = len(unique_lines)-1
        else:
            unique_lines.append(line)

    return unique_lines


def _regex_search_i(regex, lines, first):
    """Remove all except 1 line that matches the regex, ignoring whitespace.
    Returns the unique lines.

    regex: the regular expression to match
    lines: the lines of the file to deduplicate
    first: if the first match should be kept, if false, the last match is kept
    """
    unique_lines = []
    last_match = -1
    for line in lines:
        res = re.match(regex, line.strip())
        if res is not None:
            if last_match < 0:
                unique_lines.append(line)
                last_match = len(unique_lines)-1
            elif last_match >= 0 and not first:
                unique_lines.pop(last_match)
                unique_lines.append(line)
                last_match = len(unique_lines)-1
        else:
            unique_lines.append(line)

    return unique_lines


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='path', required=True, aliases=['dest', 'name']),
            regexp=dict(type='str', aliases=['regex']),
            first=dict(type='bool', default=True),
            ignore_space=dict(type='bool', default=False),
            backup=dict(type='bool', default=False)
        ),
        supports_check_mode=True,
    )

    if not os.path.isfile(module.params['dest']):
        module.exit_json(changed=False, msg='File does not exist')

    output_lines = None
    with open(module.params['dest']) as fh:
        file_lines = fh.readlines()

    if module.params['regexp'] is None:
        if module.params['ignore_space']:
            output_lines = _global_unique_search_i(file_lines)
        else:
            output_lines = _global_unique_search(file_lines)
    else:
        if module.params['ignore_space']:
            output_lines = _regex_search_i(module.params['regexp'], file_lines, module.params['first'])
        else:
            output_lines = _regex_search(module.params['regexp'], file_lines, module.params['first'])
    changed_lines = len(file_lines) - len(output_lines) 
    if module.check_mode or changed_lines == 0:
        module.exit_json(changed=changed_lines != 0, msg='{} lines removed'.format(changed_lines))

    _write_dedup_file(module, output_lines, '{} lines removed'.format(changed_lines))

if __name__ == '__main__':
    main()
