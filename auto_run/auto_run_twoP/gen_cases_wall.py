import os
import numpy as np

if not os.path.exists('template'):
    print('template case does not exist!')
    import sys
    sys.exit()

### only change the list below
rhos_list = [1.003]
k_list = [0.2]
AR_list = [0.5]
#Re_list = np.arange(8.1,9,0.1)
#Re_list= range(20,30)
Re_list = [5,7,10]
#position_tuple = [(-0.25,0.25),(-0.3,0.3),(-0.2,0.2),(-0.4,0.4)]
position_tuple = [(-0.25,0.25)]
# Note in position tuple, first value is the x position of particle 1, second value is position of particle 2, the y position keeps at 0 for both particles
euler_tuple = [(0,0),(0,45),(0,90),(0,-45),(90,90)]
###
for rhos in rhos_list:
    for k in k_list:
        for AR in AR_list:
            for Re in Re_list:
                for i in position_tuple:
                    for j in euler_tuple:
                        px_1,px_2=i
                        eulerAZ_1,eulerAZ_2 = j
                        casename = "case_2p%f_%f_Re%.1f"%(eulerAZ_1,eulerAZ_2,Re)
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

                        old_string = 'px_1'
                        new_string = '%.1f'%(px_1)
                        replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                                old_string,
                                new_string,
                                parameter_file1)
                        os.system(replace_command)

                        old_string = 'px_2'
                        new_string = '%.1f'%(px_2)
                        replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                                old_string,
                                new_string,
                                parameter_file1)
                        os.system(replace_command)

                        old_string = 'eulerAZ_1'
                        new_string = '%.1f'%(eulerAZ_1)
                        replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                                old_string,
                                new_string,
                                parameter_file1)
                        os.system(replace_command)

                        old_string = 'eulerAZ_2'
                        new_string = '%.1f'%(eulerAZ_2)
                        replace_command = "sed -i.bak \'s/%s/%s/g\' %s"%(
                                old_string,
                                new_string,
                                parameter_file1)
                        os.system(replace_command)

                        os.chdir('..')
print("Program runs successfully!")
