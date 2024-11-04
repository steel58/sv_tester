import subprocess
import json
import argparse

def add_test_bench(test_name):
    read_file = open("sv_tests.json", "r")
    contents = read_file.read()
    read_file.close()
    
    unpacked_contents = json.loads(contents)
    unpacked_contents['tests'].append(test_name)

    reserialize_contents = json.dumps(unpacked_contents)

    write_file = open("sv_tests.json", "w")
    write_file.write(reserialize_contents)
    write_file.close()

def add_source_file(file_name):
    read_file = open("sv_tests.json", "r")
    contents = read_file.read()
    read_file.close()
    
    unpacked_contents = json.loads(contents)
    unpacked_contents['source'].append(file_name)

    reserialize_contents = json.dumps(unpacked_contents)

    write_file = open("sv_tests.json", "w")
    write_file.write(reserialize_contents)
    write_file.close()

def initialize():
    file_structure = { "source": [], "tests": []}
    file_text = json.dumps(file_structure)
    file = open("sv_tests.json", "w")
    file.write(file_text)
    file.close()

def test_all():
    file = open("sv_tests.json", "r")
    contents = file.read()
    file.close()

    unpacked_contents = json.loads(contents)
    
    file_names = unpacked_contents['source']
    test_names = unpacked_contents['tests']

    subprocess.run('vlib work')

    for filepath in file_names:
        subprocess.run(f'vlog {filepath}', capture_output=True)

    for testbench in test_names:
        subprocess.run(f'vsim -c work.{testbench}', capture_output=True)
        result = subprocess.run('run -all', capture_output=True, text=True)
        print(result.stdout)

    subprocess.run('quit -f')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="initialize your sv_tester file", 
                        action="store_true")
    parser.add_argument("--add", help="adds a file or test to your sv_tester",
                        action="extend", nargs="+", type=str)
    parser.add_argument("--test", help="runs all of the test benches",
                       action="store_true")

    args = parser.parse_args()
    if args.init:
        print("Initializing")
        initialize()
    elif args.test:
        test_all()

    else:
        for string in args.add:
            print(f'Adding: {string}')
            if string.endswith(".sv"):
                add_source_file(string)
            else:
                add_test_bench(string)



main()
