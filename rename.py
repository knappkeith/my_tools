import os
import sys
import csv


def get_all_pdf_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(
        os.path.join(directory, f)) and os.path.splitext(f)[1] == '.pdf']


def parse_csv(file_name):
    names = []
    with open(file_name, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            names.append("{}_{}.pdf".format(row[1], row[0]))
    return names[1:]


def generate_rename_tuple(file_name_str):
    name_array = os.path.splitext(file_name_str)[0].split(" ")
    return (file_name_str, int(name_array[1]) - 1)


def get_all_rename_tuples(file_array):
    tuple_array = []
    for name in file_array:
        tuple_array.append(generate_rename_tuple(name))
    return tuple_array


def check_file(file_name, is_file=True):
    check_name = os.path.abspath(os.path.expanduser(file_name))
    if is_file:
        func = os.path.isfile
    else:
        func = os.path.isdir
    if func(check_name):
        return check_name
    else:
        raise ValueError


if __name__ == "__main__":
    try:
        pdf_dir = check_file(sys.argv[1], False)
        csv_file = check_file(sys.argv[2])
    except:
        print "There was an issue with your file names, use the following format:"
        print "$ python rename.py {PATH_TO_PDF_DIRECTORY} {PATH_TO_CSV_FILE}"
        sys.exit(0)

    pdfs = get_all_pdf_files(pdf_dir)
    renames = get_all_rename_tuples(pdfs)
    csv_array = parse_csv(csv_file)

    if len(renames) != len(csv_array):
        print "Arrays are not the same length, CSV: {}, PDFs: {}".format(
            len(csv_array), len(renames))
        sys.exit(0)
    else:
        for i in renames:
            old_file = os.path.join(pdf_dir, i[0])
            new_file = os.path.join(pdf_dir, csv_array[i[1]])
            os.rename(old_file, new_file)
            print "Renamed '{old_file}' ---> '{new_file}'".format(
                old_file=i[0], new_file=csv_array[i[1]])
