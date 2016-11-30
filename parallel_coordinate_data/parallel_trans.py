import os
def cutter(file_in,file_out):
	in_lines = open(file_in,'r')
	out_lines = open(file_out,'w')
	for in_line in in_lines:
		if(in_line.startswith(',')):
			out_lines.write('grade1,grade2\n')
		else:
			out_lines.write(in_line.split(',')[4] + ',' + in_line.split(',')[7])
	in_lines.close()
	out_lines.close()
for file_in in os.listdir("/home/yangliu2014/Downloads/web_vis/data"):
    if (file_in.startswith("CS") == False and file_in.endswith('.txt') == True):
        print(file_in)
	file_out = 'CS' + file_in.split('_')[0] + '-CS' + file_in.split('_')[1].split('.')[0] + '.txt'
	print (file_out)
	cutter(file_in,file_out)

