import os

# only change the list below
k_list = [0.2, 0.33, 0.4, 0.5, 0.6]
Re_list = [5, 6, 7 , 8, 10, 15, 20, 30, 40]

for k in k_list:
    for Re in Re_list:
        casename = "case_k%.2f_Re%1.f"%(k,Re)
        print(casename)
        # make case directory
        if os.path.exists(casename):
            print(casename, ' already calculated, skip!')
            continue
    
        print("generate case: ", casename)
        os.system('mkdir %s' % casename)

print("Program runs successfully!")
