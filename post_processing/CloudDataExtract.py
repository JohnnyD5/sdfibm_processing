class CloudDataExtract: 
    """
    This class extracts specifed data slices (x,y) from cloud.out file.
    # pN   - particle number to process
    # Np   - tota lnumber of particles in the clout.out file
    # Indx - Column/variable number to process
    # Tcut - Initial transient Time range to cut off 
    """
    def __init__(self, Np, pN, Tcut):
      self.Np, self.pN, self.Tcut = Np, pN, Tcut
      import numpy as np
      data=np.loadtxt('cloud.out')
      self.data=data[pN::Np]                    # data for pN extracted  
      DeltaT=self.data[1,0]-self.data[0,0]      # Sample spacing
      Tstart=int(Tcut/DeltaT);                  # Determine time start
      Tend=len(data)
      self.TStamp=[DeltaT, Tstart, Tend]
      
    def OneS(self,Indx):            #Extract one state
       data =  self.data
       #define dictionary mapping of columns in cloud.out 
       d={'0':'Time', 
       '1':'Xc', '2':'Yc', '3':'Zc', 
       '4':'Ux', '5':'Uy', '6':'Uz',
       '7':'Fx', '8':'Fy', '9':'Fz',
       '10':'Ex', 11:'Ey', '12':'Ez', 
       '13':'Ox', '14':'Oy', '15':'Oz', 
       '16':'Tx', '17':'Ty', '18':'Tz'}
       TStamp=self.TStamp
       y1=data[TStamp[1]:TStamp[2],Indx]           # Extract specific variable column Indx
       Ylabel =d[str(Indx)]
       return (y1,Ylabel)   
    
    def TwoS(self,Indx, Indy):       #Extract two states
       data =  self.data
       TStamp=self.TStamp
#define dictionary mapping of columns in cloud.out 
       d={'0':'Time', 
       '1':'Xc', '2':'Yc', '3':'Zc', 
       '4':'Ux', '5':'Uy', '6':'Uz', 
       '7':'Fx', '8':'Fy', '9':'Fz',
       '10':'Ex', 11:'Ey', '12':'Ez', 
       '13':'Ox', '14':'Oy', '15':'Oz', 
       '16':'Tx', '17':'Ty', '18':'Tz'}       
       y1=data[TStamp[1]:TStamp[2],Indx]   # Extract specific var column Indx
       y2=data[TStamp[1]:TStamp[2],Indy]   # Extract specific var column Indx
       Xlab,Ylab=d[str(Indx)], d[str(Indy)]
       return (y1,y2,Xlab,Ylab) 
       
    def time(self):                                  #Extract time
       data, TStamp =self.data, self.TStamp
       return (data[TStamp[1]:TStamp[2],0],TStamp)   # return time slice
############################    Graphs  #######################################
def StateSpace(Indx=None,Indy=None,Tcut=None, Np=None, pN=None):
    import matplotlib.pyplot as plt
    """ 
    This function plots the state space representation of two states (Indx,Indy)
    of particle (pN) in a system of particles (Np) in cloud.out file. 
    Tcut defines the initial transient that will be trimmed.
    """  
    # Initialize input not given as function argument
    if Indx is None:
        Indx=7
    if Indy is None:
        Indy=Indx+1
    if Tcut is None:
        Tcut=0
    if Np is None:
        Np=1
    if pN is None:
        pN=0
#
    y=CloudDataExtract(Np,pN,Tcut)
    X,Y,Xlabl,Ylabl=y.TwoS(Indx,Indy)
    plt.plot(X,Y)
    plt.grid()
    plt.xlabel(Xlabl)
    plt.ylabel(Ylabl)
    NpLabl=[]
    if Np>1:
        NpLabl=' Partcile No- '+str(pN)
#    
    plt.title('State Space graph - ' + Xlabl +' vs '+ Ylabl+NpLabl)
    plt.savefig('StateSpace -'+ Xlabl +' vs '+ Ylabl+NpLabl)
    plt.show()
    plt.close()
    return() 
#==============================================================================
def SParticleXYCorr(Indx=None,Indy=None,Tcut=None, Np=None, pN=None):
    import matplotlib.pyplot as plt
    from numpy import array,linspace,argmax
    from scipy.signal import correlate
    """ 
    This function computes the cross-correlation of two signals (Indx, Indy)
    of the same particle (pN) from the cloud.out file.
    Tcut defines the initial transient that will be trimmed.
    Np is the total number of particles in a simulation.
    """    
# Initialize input not given as function argument
    if Indx is None:
        Indx=7
    if Indy is None:
        Indy=Indx+1
    if Tcut is None:
        Tcut=0
    if Np is None:
        Np=1
    if pN is None:
        pN=0
#
    y=CloudDataExtract(Np,pN,Tcut)
    X,Y,Xlabl,Ylabl=y.TwoS(Indx,Indy)
    time,TStamp=y.time()
    
    sr1,dt1,mean1,sd1,rms1,skew1,kurtosis1,dur1=signal_stats(time,X,len(X))
    sr2,dt2,mean2,sd2,rms2,skew2,kurtosis2,dur2=signal_stats(time,Y,len(Y))


    cc = correlate(X,Y)

    n=len(cc)

    cc=2*cc/n

    dur=n*dt1/2;
    d=linspace( -dur, dur, n )


    idx = argmax(cc) 
    
    print (" ")
    print (" Maximum:  Delay=%8.4g sec   Amp=%8.4g " %(d[idx],cc[idx]))
  
    plt.plot(d,cc)
    plt.grid()
    plt.xlabel('Time')
    plt.ylabel(Xlabl+'x'+Ylabl)
    NpLabl=[]
    if Np>1:
        NpLabl=' Partcile No- '+str(pN)
#    
    plt.title('Cross Correlation graph - ' + Xlabl +' vs '+ Ylabl+str(NpLabl))
    plt.savefig('CrossCorr -'+ Xlabl +' vs '+ Ylabl+NpLabl)
    plt.show()
    plt.close()
    return() 
#
def MParticleXXCorr(Indx=None,Tcut=None, Np=None, pN1=None, pN2=None):
    import matplotlib.pyplot as plt
    from numpy import array,linspace,argmax
    from scipy.signal import correlate
    """ 
    This function computes the cross-correlation of the same signal (Indx)
    between two particles (pN1, pN2) from the cloud.out file.
    Tcut is to trim the initial transients
    Np is the total number of particles in a simulation.
    """
# Initialize input not given as function argument
    if Indx is None:
        Indx=7
    if Tcut is None:
        Tcut=10
    if Np is None:
        Np=1
    if pN1 is None:
        pN1=0
    if pN2 is None:
        pN2=1
#
    y1=CloudDataExtract(Np,pN1,Tcut)
    y2=CloudDataExtract(Np,pN2,Tcut)
    
    Xp1, Xlabl =y1.OneS(Indx)
    Xp2, Xlabl =y2.OneS(Indx)
    time,TStamp=y1.time()
    
    sr1,dt1,mean1,sd1,rms1,skew1,kurtosis1,dur1=signal_stats(time,Xp1,len(Xp1))
    sr2,dt2,mean2,sd2,rms2,skew2,kurtosis2,dur2=signal_stats(time,Xp2,len(Xp2))


    cc = correlate(Xp1,Xp2)

    n=len(cc)

    cc=2*cc/n

    dur=n*dt1/2;
    d=linspace( -dur, dur, n )

    idx = argmax(cc) 
    
    print (" ")
    print (" Maximum:  Delay=%8.4g sec   Amp=%8.4g " %(d[idx],cc[idx]))
  
    plt.plot(d,cc)
    plt.grid()
    plt.xlabel('Time')
    plt.ylabel(Xlabl+' for particles'+str([pN1,pN2]))
    NpLabl=' Partcile No- '+str([pN1,pN2])
#    
    plt.title('Cross Correlation graph - ' + Xlabl+NpLabl)
    plt.savefig('CrossCorr -'+ Xlabl+NpLabl)
    plt.show()
    plt.close()
    return()     
def signal_stats(a,b,num):
    """
    a is the time column.
    b is the amplitude column.
    num is the number of coordinates
    Return
          sr - sample rate
          dt - time step
        mean - average
          sd - standard deviation
         rms - root mean square
        skew - skewness
    kurtosis - peakedness
         dur - duration
    """
    from scipy import stats
    import numpy as np

    bmax=max(b)
    bmin=min(b)

    ave = np.mean(b)

    dur = a[num-1]-a[0];

    dt=dur/float(num-1)
    sr=1/dt


    rms=np.sqrt(np.var(b))
    sd=np.std(b)

    skewness=stats.skew(b)
    kurtosis=stats.kurtosis(b,fisher=False)

    print ("\n max = %8.4g  min=%8.4g \n" % (bmax,bmin))

    print ("     mean = %8.4g " % ave)
    print ("  std dev = %8.4g " % sd)
    print ("      rms = %8.4g " % rms)
    print (" skewness = %8.4g " % skewness)
    print (" kurtosis = %8.4g " % kurtosis)

    print ("\n  start = %8.4g sec  end = %8.4g sec" % (a[0],a[num-1]))
    print ("    dur = %8.4g sec \n" % dur)
    return sr,dt,ave,sd,rms,skewness,kurtosis,dur
#==============================================================================    
def HistG(Indx=None, Tcut=None, Np=None, pN=None):
    import matplotlib.pyplot as plt
    import statistics
# Initialize input not given as function argument
    if Indx is None:
        Indx=7
    if Tcut is None:
        Tcut=0
    if Np is None:
        Np=1
    if pN is None:
        pN=0
#
    y=CloudDataExtract(Np,pN,Tcut)
    X, Xlab =y.OneS(Indx)
    Ylab = '# Occurence'
    ###################
    # Analyze Selected data, Indx
    ###################
    X_mean = statistics.mean(X)
    X_max=max(X)
    X_min=min(X)
    X_amp = X_max-X_min
    plt.hist(X,30)
    NpLabl=[]
    if Np>1:
        NpLabl=' Partcile No- '+str(pN)    
    plt.title('Histogram of '+ Xlab+NpLabl)
    plt.xlabel(Xlab)
    plt.ylabel(Ylab)
    plt.legend(['Mean - '+ str(X_mean)], loc='upper left' )
    plt.savefig('Histogram-'+ Xlab+NpLabl)
    plt.show()
    plt.close()
    return()

def Tser(Indx=None, Tcut=None, Np=None, pN=None):
    import matplotlib.pyplot as plt
    import statistics
# Initialize input not given as function argument
    if Indx is None:
        Indx=7
    if Tcut is None:
        Tcut=0
    if Np is None:
        Np=1
    if pN is None:
        pN=0
#
    y=CloudDataExtract(Np,pN,Tcut)
    X, Ylab =y.OneS(Indx)
    Xlab = 'Time'
    time,TStamp=y.time()
    Mean = statistics.mean(X)
#
    plt.plot(time, X)          # plot variable
    NpLabl=[]
    if Np>1:
        NpLabl=' Partcile No- '+str(pN)
    plt.title(Xlab+' vs '+Ylab+NpLabl)
    plt.legend(['Mean - '+Ylab + str(Mean)], loc='upper left' )
    plt.xlabel(Xlab)
    plt.ylabel(Ylab)
    plt.savefig('TimeSer '+Ylab+NpLabl)
#
    plt.show()
    plt.close()
    return() 

def Pspec(Indx=None, Tcut=None, Np=None, pN=None):
    import numpy as np
    import math
    import matplotlib.pyplot as plt
    import statistics
    from scipy.fftpack import fft
    sign = lambda x: math.copysign(1, x)
#
    # Initialize input not given as function argument
    if Indx is None:
        Indx=7
    if Tcut is None:
        Tcut=0
    if Np is None:
        Np=1
    if pN is None:
        pN=0
    y=CloudDataExtract(Np,pN,Tcut)
    X, Ylab =y.OneS(Indx)

    time,TStamp=y.time()
    ###################
    # Analyze Selected data, Indx
    ###################
    X_mean = statistics.mean(X)
    X_zero_mean=X-X_mean                        #zero mean
    N=len(X_zero_mean)                          # number of data points
    X_max=max(X_zero_mean)
    X_min=min(X_zero_mean)
    X_amp = X_max-X_min
    print(Ylab +' - Amplitude = %g, Mean= %g ' % (X_amp, X_mean))
#
    T=[]
    for i in range(1, N-1):
       if (sign(X_zero_mean[i])*sign(X_zero_mean[i+1])) < 0:
         T.append(time[i])
    #print('Zero Crossing:\n', T)
    WaveLength=[]
    for i in range(1,len(T)-1):
       WaveLength.append(T[i+1]-T[i])
    #print('Time between zero Corssing:\n',WaveLength)
    WaveLength_avg=2.0*statistics.mean(WaveLength)
    print('Wavelength from zero crossing: ', WaveLength_avg )
    print('Freq from zero crossing:  ',1.0/WaveLength_avg)
    ###################
    # Generate power spectrum
    ###################    
    Xfft=fft(X_zero_mean);
    XP=2/N*np.abs(Xfft[0:N//2])
    Xf=np.linspace(0,1/(2*TStamp[0]),N//2)
    Temp=list(XP);
    X_freq=Xf[Temp.index(max(Temp))]
    print('Freq from fft:  ',X_freq)
    plt.xlim(0,2)
    plt.plot(Xf,XP)
    plt.grid()
    plt.xlabel('Frequency')
    plt.ylabel('Power Spec')
    NpLabl=[]
    if Np>1:
        NpLabl=' Partcile No- '+str(pN)
    plt.title('Power Spectra signal - '+Ylab+ '  '+str(X_freq)+NpLabl)
    plt.legend(['Freq='+Ylab])
    plt.savefig('PowerSpec-'+Ylab+NpLabl)
    plt.show()
    plt.close()
    return() 
##############################################################   
def parabola(vmax,N):
    import numpy as np
    import matplotlib.pyplot as plt
    x=np.linspace(-0.5,0.5,N)
    y=vmax*(1-(x/0.5)**2)
    f = open("UProfile.csv",'w')    # open file in current directory
    for i in range(0,len(x)):
        line=str(x[i])+',0.0,'+str(y[i])+',0.0'+'\n'
        f.write(line)
    f.close()
    print(x,y)
    plt.plot(x,y)
    plt.show()
##############################################################  
def RegCavity(N):
    import numpy as np
    import matplotlib.pyplot as plt
    x=np.linspace(0,1,N)
    y=(1-(2*x-1)**18)**2
    f = open("UProfile.csv",'w')    # open file in current directory
    for i in range(0,len(x)):
        line=str(x[i])+','+str(y[i])+',0.0,0.0'+'\n'
        f.write(line)
    f.close()    
    print(x,y)
    plt.plot(x,y)
    plt.show()
############################################################## 