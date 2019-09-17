import os
import numpy as np

if not os.path.exists('template'):
    print('template case does not exist!')
    import sys
    sys.exit()

### only change the list below
rhos_list = [1.003]
k_list = [0.4]
AR_list = [0.75]
#Re_list = np.arange(8.1,9,0.1)
#Re_list= range(20,30)
Re_list = [35,40,45,50,55,60]
###
for rhos in rhos_list:
    for k in k_list:
        for AR in AR_list:
            for Re in Re_list:
                casename = "case_rhos%.1f_k%.2f_AR%.2f_Re%.1f"%(rhos,k,AR,Re)
                print(casename)
                # make case directory
                if os.path.exists(casename):
                    print(casename, ' already calculated, skip!')
                    continue

                print("generate case: ", casename)
                os.system('cp -R template %s' % casename)

                # change to case directory and make modification to parameters
                os.chdir(casename)

                parameter_file1 = './solidDict'
                parameter_file2 = './constant/transportProperties'
                parameter_file3 = './job.pbs'
                parameter_file4 = './system/blockMeshDict'
            # Note!!! nu=1.0/Re is for one plane moving and fluid rho is 1
            # Note!!! nu=2.0/Re is for both plane moving and fluid rho is 1
                #nu = 1.0/Re/20
                old_string = 'ra_val'
                new_string = '%.6f' % (k/2)
                replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                        old_string,
                        new_string,
                        parameter_file1)
                os.system(replace_command)

                rb = k/2*AR
                old_string = 'rb_val'
                new_string = '%.6f' % (rb)
                replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                        old_string,
                        new_string,
                        parameter_file1)
                os.system(replace_command)

                old_string = 'rhos_val'
                new_string = '%.6f' % (rhos)
                replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                        old_string,
                        new_string,
                        parameter_file1)
                os.system(replace_command)

                old_string = 'nu_val'
                new_string = '%.6f' % (2*(k/2)**2/Re)
                replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                        old_string,
                        new_string,
                        parameter_file2)
                os.system(replace_command)

                old_string = 'name_val'
                new_string = casename
                replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                        old_string,
                        new_string,
                        parameter_file3)
                os.system(replace_command)

                nc_H = 30/(2*rb)
                old_string = 'nc_H'
                new_string = '%1.f'%(nc_H)
                replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                        old_string,
                        new_string,
                        parameter_file4)
                os.system(replace_command)

                old_string = 'nc_L'
                new_string = '%1.f'%(nc_H+200)
                replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                        old_string,
                        new_string,
                        parameter_file4)
                os.system(replace_command)

                os.chdir('..')
print("Program runs successfully!")
