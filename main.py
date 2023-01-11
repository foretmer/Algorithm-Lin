import xlrd2
from Cargo import*
from Container import*
from Init import*
import datetime
import xlrd
if __name__ == "__main__":
        list = xlrd2.open_workbook('data/list.xlsx')
        sheet = list.sheet_by_index(0)
        case = Container(587, 233, 220)
        for i in range(1,26):
            j = 0
            cargos = []
            while (sheet.cell_type(i, j) != 0):
                l = int(sheet.cell_value(i, j))
                w = int(sheet.cell_value(i, j + 1))
                h = int(sheet.cell_value(i, j + 2))
                c = int(sheet.cell_value(i, j + 3))
                cargos.extend(Cargo(l, w, h) for _ in range(c))
                j += 4
                if j >= 60 : break #excel中只有60列，超过会报错
            start = datetime.datetime.now()
            rate = encase_cargos_into_container(cargos, case, VolumeGreedyStrategy)
            print("填充率：",rate)
            end = datetime.datetime.now()
            print("执行时间：",end-start,"\n具体坐标见",i,"_encasement.csv文件\n")
            case.save_encasement_as_file(i,rate,end-start)



