import re


def process_line(line):
    return re.sub(r"NumberInt\((\d+)\)", r"\1", line)


def remove_numberint(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f_in:
        with open(output_file, "w", encoding="utf-8") as f_out:
            for line in f_in:
                f_out.write(process_line(line))


input_filename = "dblpv13.json"
output_filename = "dblpv13_cleaned.json"
remove_numberint(input_filename, output_filename)
