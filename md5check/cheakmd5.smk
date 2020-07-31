import os

#####################################################################
#                            config
path_input_file_list = "test/file.list"  # The file you need to check
path_orignal_md5 = "test/orginal.md5"
path_workspace = "test/working/"
project_name = "test"
institution = "XJTU"
author = "PJ"
#####################################################################
#                            prepossessing

file_dict = {}
for line in open(path_input_file_list):
    file_path = line[:-1]
    file_dict[file_path.split("/")[-1]] = file_path


#####################################################################
#                            useful function
def get_file_path(wildcards):
    return file_dict[wildcards.file_id]


#####################################################################
#                            output
output_list = [path_workspace + project_name + "_" + institution + "_" + author + ".md5"]
if len(path_orignal_md5) > 0 and os.path.exists(path_orignal_md5):
    output_list += [path_workspace + project_name + "_" + institution + "_" + author + ".report"]
    output_list += [path_workspace + project_name + "_" + institution + "_" + author + ".failed"]
    output_list += [path_workspace + project_name + "_" + institution + "_" + author + ".conflict"]

rule all:
    input:
         output_list

rule generate_md5:
    input:
         get_file_path
    output:
          path_workspace + "detail/{file_id}.md5"
    run:
        shell("md5sum {input} >{output}")
rule check_md5_merge:
    input:
         expand([path_workspace + "detail/{file_id}.md5"], file_id=file_dict.keys())
    output:
          path_workspace + project_name + "_" + institution + "_" + author + ".md5"
    run:
        shell("cat {input} >{output}")

rule check_md5:
    input:
         orginal=path_orignal_md5,
         my_md5=path_workspace + project_name + "_" + institution + "_" + author + ".md5"
    output:
          report=path_workspace + project_name + "_" + institution + "_" + author + ".report",
          failed=path_workspace + project_name + "_" + institution + "_" + author + ".failed",
          conflict=path_workspace + project_name + "_" + institution + "_" + author + ".conflict",
    run:
        file_report = open(output.report, "w")
        file_failed = open(output.failed, "w")
        file_conflict = open(output.conflict, "w")
        orginal = {}
        check_id = {}
        for line in open(input.orginal):
            lineinfo = line[:-1].split(" ")  # two space in md5 file
            md5 = lineinfo[0]
            file_path = lineinfo[-1]
            file_id = lineinfo[-1].split("/")[-1]
            if file_id in check_id:
                check_id.append(file_id)
            else:
                orginal[file_id] = md5
        num = 0
        failed_num = 0
        conflict_num = 0

        for line in open(input.my_md5):
            num += 1
            lineinfo = line[:-1].split(" ")  # two space in md5 file
            md5 = lineinfo[0]
            file_path = lineinfo[-1]
            file_id = lineinfo[-1].split("/")[-1]
            if file_id in check_id:
                file_conflict.write(md5 + "  " + file_path + "\n")
                conflict_num += 1
            else:
                if md5 != orginal[file_id]:
                    file_failed.write(md5 + "  " + file_path + "\n")
                    failed_num += 1
        file_failed.close()
        file_conflict.close()
        file_report.write("Total: " + str(num) + "\n")
        file_report.write("Succeed: " + str(num - failed_num - conflict_num) + "\n")
        file_report.write("Failed: " + str(failed_num) + "\n")
        file_report.write("Conflict: " + str(conflict_num) + "\n")
        file_report.close()
