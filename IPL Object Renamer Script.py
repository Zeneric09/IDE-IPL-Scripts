import glob, os

def get_files_in_directory(str_extension):
    return glob.glob(f"./*{str_extension}")

def get_files_in_game_directory(root_dir, str_extension):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(str_extension):
                file_list.append(os.path.join(dirpath, filename))
    return file_list

def process_ide_files(func_ide_list):
    id_name_map = {}
    for x in func_ide_list:
        with open(x, 'r') as ide:
            valid_line = False
            for line in ide:
                line = line.strip()
                if line.startswith(("objs", "tobj")):
                    valid_line = True
                if valid_line and not (line.startswith('#') or not line or line[0].isalpha()):
                    data = line.split(',')
                    if len(data) >= 2:
                        id_name_map[data[0].strip()] = data[1].strip()
                if line.startswith("end"):
                    valid_line = False
    return id_name_map

def is_inst_line(ipl_line):
    if ipl_line.startswith("end"):
        return "inst end"
    elif not (ipl_line.startswith('#') or not ipl_line or ipl_line[0].isalpha()):
        return True
    return False

def get_id_name(func_line):
    if func_line.strip():
        return func_line.strip().split(',')

def process_ipl_files(func_ipl_list, id_name_map):
    for index, y in enumerate(func_ipl_list):
        temp_ipl_lines = []
        with open(y, 'r') as ipl:
            for line in ipl:
                line = line.rstrip()
                if is_inst_line(line) == "inst end":
                    temp_ipl_lines.append("end")
                    temp_ipl_lines.extend(ipl)
                    break
                elif is_inst_line(line):
                    ipl_line = get_id_name(line)
                    if ipl_line and ipl_line[0] in id_name_map:
                        ipl_line[1] = id_name_map[ipl_line[0]]
                        line = ",".join(ipl_line)
                temp_ipl_lines.append(line)
        # Overwrite the original file with updated content
        with open(y, 'w') as outfile:
            outfile.write("\n".join(temp_ipl_lines) + "\n")
    print("Renaming finished successfully.")

def main():
    print("IPL Object Renamer Script\nAuthor: Grinch_\nContact: user.grinch@gmail.com\nUsage: Put all your ipl files in this dir and press any key to run this script.")
    game_dir = input("\nProvide path to ide files (game directory, no quotes): ")
    ipl_files_list = get_files_in_directory(".ipl")
    ide_files_list = get_files_in_game_directory(game_dir, ".ide")
    if ide_files_list and ipl_files_list:
        print("\n--------------------\nIDE files found:", len(ide_files_list), "\nIPL files found:", len(ipl_files_list), "\n--------------------\n")
        input("\nPress any key to proceed")
        print("\nThis might take a while depending on the file count and size. Please be patient...\n\n--------------------------------------------------\n")
        id_name_map = process_ide_files(ide_files_list)
        process_ipl_files(ipl_files_list, id_name_map)
    else:
        print("Necessary files are missing, exiting...")
    input("\nPress any key to proceed")

if __name__ == "__main__":
    main()
