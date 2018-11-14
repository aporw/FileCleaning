import xlrd
d1 = {}
d2={}
wb = xlrd.open_workbook('C:\Users\pankur\Downloads\Cleanup prod client list.xlsx')
sh = wb.sheet_by_index(0)
for i in range(1,16):
    cell_value_domain = sh.cell(i,0).value
    cell_value_db = sh.cell(i,2).value
    cell_value_retention=sh.cell(i,1).value
    d1[cell_value_domain] = cell_value_db
    d2[cell_value_domain] = cell_value_retention
retention = []
db = []
for key in d1:
    domains = key
    #print domains
    db.append(d1[key])
    retention.append(d2[key])

print retention