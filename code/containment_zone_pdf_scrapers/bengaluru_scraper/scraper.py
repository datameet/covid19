import os
from datetime import date
import tabula

#change cwd so script can be run from wherever
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

os.chdir("../../../" )
today = date.today()

# format date to standard
today_date = today.strftime("%Y_%m_%d")

#Get start and end range for pages. This range is inclusive.
start_range = input("Start Page:")
end_range = input("End Page:")

pdf_name = input("File Name (without .pdf at the end):")
data_date = input("What date is this data current to? (YY_MM_DD)")
pdf_path = "./downloads/city-containment-zones-backup/bengaluru/"
output_path = "./data/containment_zones/bengaluru"


tabula.convert_into(pdf_path + pdf_name + ".pdf", output_path + "_" + data_date + ".csv", output_format="csv", pages= start_range +  "-" + end_range, stream=True)


