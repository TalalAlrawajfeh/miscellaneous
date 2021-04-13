import os
import re


def enhance(title):
    result = title
    patterns = ['[a-z][A-Z]', '[A-Z][A-Z]']
    for pattern in patterns:
        for match in re.finditer(pattern, title):
            text = match.group(0)
            if text == 'IV' or text == 'VI' or text == "II":
                continue
            result = result.replace(text, text[:1] + ' ' + text[1:])
    return result


def get_date(file_name):
    file_body = file_name[:file_name.find('.pdf')]
    date_index = 0
    while date_index < len(file_body):
        if file_body[date_index:date_index + 1].isnumeric():
            break
        date_index += 1
    if date_index == len(file_body):
        return ''
    end_index = date_index + 1
    while end_index < len(file_body):
        if not file_body[end_index:end_index + 1].isnumeric():
            break
        end_index += 1
    return file_body[date_index:end_index]


def main():
    file_paths = all_file_paths()
    commands = ''
    for file_pair in file_paths:
        file_path = file_pair[1]
        file = open(file_path, 'r')
        lines = file.readlines()
        file.close()
        copyright_index = find_copyright_index(lines)
        if copyright_index == -1:
            print("Format Error!")
            return
        while len(lines) > copyright_index:
            lines.pop()
        last_line = lines.pop().strip()
        if re.search('[A-Za-z]', last_line) is None:
            last_line = lines.pop().strip()
        title = join_with_max_length(lines, 90) + suffix_to_title_appendage(
            file_pair[0]) + ' - Jonathan Bennett (' + last_line + ' ' + get_date(file_pair[0]) + ')'
        commands += 'mv ' + file_pair[0][:file_pair[0].find('.txt')] + ' "' + enhance(title) + '.pdf"\n'
    print(commands)


def join_with_max_length(lines, max_length):
    result = ''
    i = 0
    while i < len(lines) and len(result) < max_length:
        result += lines[i].strip() + ' '
        i += 1
    return result.rstrip()


def find_copyright_index(lines):
    for i in range(0, len(lines)):
        if lines[i].strip().lower().startswith('copyright'):
            return i
    return -1


def all_file_paths():
    file_paths = []
    for currentDirectory, directories, files in os.walk(os.curdir):
        file_paths += [(file, os.path.join(currentDirectory, file)) for file in files if file.endswith('.txt')]
    file_paths.sort(key=lambda x: x[0])
    return file_paths


def suffix_to_title_appendage(file_name):
    appendage = ' '
    file_body = file_name[:file_name.find('.pdf')]

    appendage += get_part('essay', file_body)
    appendage += get_part('book', file_body)
    appendage += get_part('part', file_body)
    appendage += get_part('chapter', file_body)
    appendage += get_part('section', file_body)
    # appendage += section_letter(file_body)

    underscore_index = file_body.rfind('_')
    if underscore_index != -1:
        appendage += '[' + file_body[underscore_index + 1:] + ']'

    if appendage.strip() == '':
        return ''
    else:
        return appendage.rstrip()


def get_part(part_name, file_body):
    part_index = file_body.rfind(part_name)
    if part_index != -1:
        part_index += len(part_name)
        end_index = part_index + 1
        while end_index < len(file_body) and file_body[part_index:end_index].isnumeric():
            end_index += 1
        if end_index != len(file_body):
            end_index -= 1
        return part_name[:1].upper() + part_name[1:] + '(' + file_body[part_index:end_index] + ') '
    return ''


def section_letter(file_body):
    last_char = file_body[len(file_body) - 1:]
    if re.match('[a-z]', last_char) is not None:
        return '(' + last_char.upper() + ') '
    return ''


if __name__ == '__main__':
    main()
