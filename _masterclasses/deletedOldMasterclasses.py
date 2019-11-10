from pathlib import Path
from datetime import date
from typing import Generator


def get_start_date_from_file(file: Path) -> date:
    """
    Get the startDate parameter from a markdown file
    :param file: Path of file to parse
    :return: Date read from the startDate parameter of the file
    """
    output_date = date(year=9999, month=1, day=1)

    with open(str(file)) as file_pointer:

        number_of_triple_dash_lines = 0

        for line in file_pointer.readlines():

            trimmed_line = line.strip()

            if trimmed_line.startswith('startDate') or trimmed_line.startswith('endDate'):
                try:
                    split_trimmed_line = trimmed_line.split(':')
                    _, start_date_string = split_trimmed_line

                    # Extract year, month and day from the date string#
                    split_start_date = start_date_string.split('-')

                    year, month, day = map(lambda x: int(x), split_start_date)
                    output_date = date(year=year, month=month, day=day)
                except:
                    print("Date formatting error in file: ", file)
                    continue

            # The header of our files is marked by three dashes.
            # Thats why we know that the second triple of dashes marks the end of the header
            # and we can continue with the next file
            if trimmed_line == '---':
                number_of_triple_dash_lines += 1

            if number_of_triple_dash_lines > 1:
                break

    # If something went wrong return date very far in the future, so file will not be deleted
    return output_date


if __name__ == '__main__':
    masterclass_files = Path.cwd().glob('*.md')  # type: Generator

    deleted_at_least_one_file = False  # type: bool

    print("Looking for old masterclasses ...")

    for masterclass_file in masterclass_files:

        start_date = get_start_date_from_file(masterclass_file)

        if start_date < date.today():
            print("Deleted: ", masterclass_file)
            masterclass_file.unlink()
            deleted_at_least_one_file = True

    if not deleted_at_least_one_file:
        print("No old masterclasses found. No files were deleted.")
