import os
def cutter(file_in,file_out,pre,post):
	in_lines = open(file_in,'r')
	out_lines = open(file_out,'w')
	for in_line in in_lines:
		if(in_line.startswith(',')):
			out_lines.write('CS'+pre+',CS' + post + '\n')
		else:
			out_lines.write(in_line.split(',')[4] + ',' + in_line.split(',')[7])
	in_lines.close()
	out_lines.close()
for file_in in os.listdir("/home/yangliu2014/Downloads/web_vis/parallel_coordinate_data"):
    if (file_in.startswith("CS") == False and file_in.endswith('.txt') == True):
        print(file_in)
	pre = file_in.split('_')[0]
	post = file_in.split('_')[1].split('.')[0]
	file_out = 'CS' + file_in.split('_')[0] + '-CS' + file_in.split('_')[1].split('.')[0] + '.txt'
	print (file_out)
	cutter(file_in,file_out,pre,post)

