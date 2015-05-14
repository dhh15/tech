from sys import argv

script, source_file, end_file = argv

with open(source_file, 'r') as source:
	target = open(end_file, 'w')
	
	to_file = '{"Place names" : ['
	
	for line in source:
		kirjoitettava = line.split("\t")[0].replace("*", "") #take only the Swedish name and delete * chars
		kirjoitettava = kirjoitettava[:-1] #cut off the last char = space
		to_file += '"' + kirjoitettava + '", '
	to_file = to_file[:-2]
	to_file += "] }"
	target.write(to_file)
target.close()
