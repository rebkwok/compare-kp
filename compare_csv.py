import click
import csv
import os
import pprint


@click.command()
@click.argument('file1')
@click.argument('file2')
def compare(file1, file2):
    with open(file1) as csvfile:
        csv1 = csv.DictReader(csvfile)
        csv1_dict = dict(
            (item['Title'].replace(' ', '_'), item)
            for item in csv1 if item['Group'] != 'Root/Backup'
        )
    with open(file2) as csvfile:
        csv2 = csv.DictReader(csvfile)
        csv2_dict = dict(
            (item['Title'].replace(' ', '_'), item)
            for item in csv2 if item['Group'] != 'Root/Backup'
        )

    missing_in_file1 = set(csv2_dict) - set(csv1_dict)
    missing_in_file2 = set(csv1_dict) - set(csv2_dict)
    present_in_both = set(csv1_dict) & set(csv2_dict)

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

    mismatch = False
    for item in present_in_both:
        if csv1_dict[item] != csv2_dict[item]:
            print('{} does not match'.format(item))
            print(file1)
            print(csv1_dict[item])
            print(file2)
            print(csv2_dict[item])
            mismatch = True

    if not missing_in_file1 and not missing_in_file2 and not mismatch:
        print('Files match')

if __name__ == '__main__':
    compare()
