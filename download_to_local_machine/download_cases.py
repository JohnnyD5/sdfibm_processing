import os

# only change the list below
k_list = [0.2, 0.33, 0.4, 0.5, 0.6]
Re_list = [5, 6, 7 , 8, 10, 15, 20, 30, 40]

for k in k_list:
    for Re in Re_list:
        casename = "case_k%.2f_Re%1.f"%(k,Re)
        print(casename)
        os.chdir(casename)
        os.system('cp cloud.out ../download/%s/'% casename)
        os.system('cp -r 0 ../download/%s/'% casename)
        os.system('cp -r constant ../download/%s/'% casename)
        os.system('cp -r system ../download/%s/'% casename)
        os.system('cp solidDict ../download/%s/'% casename)
        os.chdir('..')
print("Program runs successfully!")
