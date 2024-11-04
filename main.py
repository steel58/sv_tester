import subprocess
import argparse
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="the path of the .do file to execute",
                        type=str)

    args = parser.parse_args()
    result = subprocess.run(f'vsim -c -do {args.filepath}', capture_output=True, text=True)
    lines = result.stdout.split('\n')
    output_filter = "^# (Loading|do|Model|Start|End| {3}Time:|Break in Module|vlog|Top|10.5b)|vlib-34|\$stop|^# $|Reading C:"
    for line in lines:
        useless = re.search(output_filter, line)
        if useless is None:
            print(line)
            if line.startswith("# Errors: "):
                print()



main()
