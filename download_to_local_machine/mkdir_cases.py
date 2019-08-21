import os

# only change the list below
rhos_list = [1.003]
k_list = [0.2]
AR_list = [0.5]
Re_list = [7,7.2,7.3,7.4,7.6,7.8,8,8.5]
###
for rhos in rhos_list:
    for k in k_list:
        for AR in AR_list:
            for Re in Re_list:
                casename = "case_rhos%.1f_k%.1f_AR%.1f_Re%.1f"%(rhos,k,AR,Re)

        print(casename)
        # make case directory
        if os.path.exists(casename):
            print(casename, ' already calculated, skip!')
            continue

        print("generate case: ", casename)
        os.system('mkdir %s' % casename)

print("Program runs successfully!")
