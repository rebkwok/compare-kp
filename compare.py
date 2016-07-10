import ast
import click
import os


def parse(file):
    """Parse a KeePass txt export to a dictionary"""

    f = open(file, 'r')
    lines = [line.strip() for line in f.readlines()]
    f.close()

    stripped = []
    skip = False
    for line in lines:
        if line.startswith('*** Group: Backup ***'):
            skip = True
        elif line.startswith('***'):
            skip = False

        if not skip:
            if line.startswith('Title:'):
                stripped.append(line)
            elif line.startswith('Username:'):
                stripped.append(line)
            elif line.startswith('Url:'):
                stripped.append(line)
            elif line.startswith('Comment:'):
                stripped.append(line)
            elif line.startswith('Password:'):
                stripped.append(line)

    groups = [group for group in zip(*(iter(stripped),) * 5)]

    kp_dict = {}
    for i, group in enumerate(groups):
        group_dict = dict([[it.strip() for it in item.split(':', 1)] for item in group])
        if group_dict['Title'] in kp_dict:
            kp_dict['{} (duplicate)'.format(group_dict['Title'], i)] = group_dict
        else:
            kp_dict[group_dict['Title']] = group_dict
    return kp_dict


@click.command()
@click.argument('file1')
@click.argument('file2')
def compare(file1, file2):
    parsedfile1 = parse(file1)
    parsedfile2 = parse(file2)
    missing_in_file1 = set(parsedfile2) - set(parsedfile1)
    missing_in_file2 = set(parsedfile1) - set(parsedfile2)
    present_in_both = set(parsedfile1) & set(parsedfile2)

    for item in missing_in_file1:
        print(
            '{} in {} does not exist in {}'.format(
                item, os.path.split(file2)[-1], os.path.split(file1)[-1]
            )
        )

    for item in missing_in_file2:
        print(
            '{} in {} does not exist in {}'.format(
                item, os.path.split(file1)[-1], os.path.split(file2)[-1]
            )
        )

    for item in present_in_both:
        if parsedfile1[item] != parsedfile2[item]:
            print('{} does not match'.format(item))

if __name__ == '__main__':
    compare()