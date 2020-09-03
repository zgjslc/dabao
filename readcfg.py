class readcfg:
    def readfile(self,filename):
        self.ROTX = []
        self.DPCENT = []
        self.DPAXIS = []
        self.DPLAW = []
        self.DPZONE = []
        self.HYLD = []
        self.TRNS = ' '
        self.ROTYZTYPE = ' '
        self.ROTYZ = ' '
        self.GZZONE = []
        A = ' '
        self.NMSH = A
        self.MTYP = A
        self.NMRK = A
        self.NPRT = A
        self.NCSY = A
        self.NROT = A
        self.NSLD = A
        self.NSTP = A
        self.DELT=self.LDTYPE=self.TLTYPE=self.XUSUAN=self.LLMA=self.LLYJ=self.LLLNS=self.LLCKCD=self.QDCD=\
        self.QDMJ=self.QDZX=self.QDZBX=self.QJDL=self.QJTJ=self.QJCFL=self.QJCFL3=self.LDSIMTYPE=self.JSOUT=\
        self.JSINNER=self.JSINONE=self.JSCANZHI=self.YXCANZHI=self.JSNT=self.YXJIEGUO=self.YXXUSUAN=A


        filepath = filename
        if(filepath !=''):
            with open(filepath, 'r') as file_read:
                while True:
                    lines = file_read.readline()
                    if not lines:
                        break
                        pass
                    if (lines.startswith('#NMSH')):
                        s = lines.split()
                        self.NMSH = s[1]
                    if (lines.startswith('#MTYP')):
                        s = lines.split()
                        self.MTYP = ''
                        for i in range(int(self.NMSH)):
                            self.MTYP = self.MTYP + str(s[i + 1]) + ' '
                    if (lines.startswith('#NMRK')):
                        s = lines.split()
                        self.NMRK = ''
                        for i in range(int(self.NMSH)):
                            self.NMRK = self.NMRK + str(s[i + 1]) + ' '
                    if (lines.startswith('#NPRT')):
                        s = lines.split()
                        self.NPRT = ''
                        for i in range(int(self.NMSH)):
                            self.NPRT = self.NPRT + str(s[i + 1]) + ' '
                    if (lines.startswith('#TRNS')):
                        s = lines.split()
                        self.TRNS = ''
                        for i in range(3):
                            self.TRNS = self.TRNS + str(s[i + 1]) + ' '
                    if (lines.startswith('#NCSY')):
                        s = lines.split()
                        self.NCSY = s[1]
                    if (lines.startswith('#CSYS')):
                        s = lines.split('#ROTX(')
                        s = s[1].split(') #')
                        self.ROTX.append(s[0])
                        if ('ROTY' in lines):
                            self.ROTYZTYPE = 'Y'
                            s = lines.split('#ROTY(')
                            s = s[1].split(')')
                            self.ROTYZ = s[0]
                        if ('ROTZ' in lines):
                            self.ROTYZTYPE = 'Z'
                            s = lines.split('#ROTZ(')
                            s = s[1].split(')')
                            self.ROTYZ = s[0]
                        s = lines.split('#ZONE(')
                        s = s[1].split(')')
                        self.GZZONE.append(s[0])
                    if (lines.startswith('#NROT')):
                        s = lines.split()

                        self.NROT = s[1]
                    if (lines.startswith('#ROTA')):
                        s = lines.split('#CENT(')
                        s = s[1].split(')')
                        self.DPCENT.append(s[0])
                        s = lines.split('#AXIS(')
                        s = s[1].split(')')
                        self.DPAXIS.append(s[0])
                        s = lines.split('#RPOP(')
                        s = s[1].split(')')
                        self.DPLAW.append(s[0])
                        s = lines.split('#ZONE(')
                        s = s[1].split(')')
                        self.DPZONE.append(s[0])
                    if (lines.startswith('#NSLD')):
                        s = lines.split()
                        self.NSLD = s[1]
                    if (lines.startswith('#SLID')):
                        s = lines.split()
                        self.HYLD.append(s[1])
                    if (lines.startswith('#UNST')):
                        s = lines.split('#NSTP(')
                        s = s[1].split(')')
                        self.NSTP = s[0]
                        s = lines.split('#DELT(')
                        s = s[1].split(')')
                        self.DELT = s[0]
                    if (lines.startswith('PHYSICAL_PROBLEM')):
                        self.LDTYPE = self.setzhi(lines)
                    if (lines.startswith('TURB_MODEL')):
                        self.TLTYPE = self.setzhi(lines)
                    if (lines.startswith('IS_RESTART_SOL')):
                        self.XUSUAN = self.setzhi(lines)
                    if (lines.startswith('FLOW_MACH')):
                        self.LLMA = self.setzhi(lines)
                    if (lines.startswith('FLOW_AOA')):
                        self.LLYJ = self.setzhi(lines)
                    if (lines.startswith('REYNOLDS_NUMBER')):
                        self.LLLNS = self.setzhi(lines)
                    if (lines.startswith('REYNOLDS_LENGTH')):
                        self.LLCKCD = self.setzhi(lines)
                    if (lines.startswith('AERO_REFLEN')):
                        self.QDCD = self.setzhi(lines)
                    if (lines.startswith('AERO_REFAREA')):
                        self.QDMJ = self.setzhi(lines)
                    if (lines.startswith('AERO_REFCENT')):

                        s = lines.split('=')
                        s = s[1].split()
                        a1= float(s[0])
                        a2 = float(s[1])
                        a3 = float(s[2])
                        self.QDZX = str(a1)+' '+str(a2)+' '+str(a3)
                    if (lines.startswith('AERO_REFCSID')):
                        self.QDZBX = self.setzhi(lines)
                    if (lines.startswith('CONV_NUM_METHOD_FLOW')):
                        self.QJDL = self.setzhi(lines)
                    if (lines.startswith('TEMPORAL_SCHEME')):
                        self.QJTJ = self.setzhi(lines)
                    if (lines.startswith('CFL_NUMBER')):
                        self.QJCFL = self.setzhi(lines)
                    if (lines.startswith('CFL_RAMP')):
                        s = lines.split('=')
                        s = s[1].split()
                        a1 = float(s[0])
                        a2 = float(s[1])
                        a3 = float(s[2])
                        self.QJCFL3 = str(a1) + ' ' + str(a2) + ' ' + str(a3)
                    if (lines.startswith('UNSTEADY_SIMULATION')):
                        self.LDSIMTYPE = self.setzhi(lines)
                    if (lines.startswith('NITER_OUTER')):
                        self.JSOUT = self.setzhi(lines)
                    if (lines.startswith('NITER_INNER')):
                        self.JSINNER = self.setzhi(lines)
                    if (lines.startswith('NITER_INONE')):
                        self.JSINONE = self.setzhi(lines)
                    if (lines.startswith('RES_CONV_ORDER')):
                        self.JSCANZHI = self.setzhi(lines)
                    if (lines.startswith('NITER_RESHOW')):
                        self.YXCANZHI = self.setzhi(lines)
                    if (lines.startswith('NITER_PRLOOP')):
                        self.JSNT = self.setzhi(lines)
                    if (lines.startswith('NITER_RUSAVE')):
                        self.YXJIEGUO = self.setzhi(lines)
                    if (lines.startswith('NITER_RESOLU')):
                        self.YXXUSUAN = self.setzhi(lines)
                    if (lines.startswith('/')):
                        pass
                else:
                    print('时空机')
                    pass
        return self.NMSH,self.MTYP,self.NMRK,self.NPRT,self.TRNS,self.NCSY,self.ROTX,self.ROTYZTYPE,self.ROTYZ,\
    self.NROT,self.DPCENT,self.DPAXIS,self.DPLAW,self.DPZONE,self.NSLD,self.HYLD,self.NSTP,self.DELT,self.LDTYPE,\
    self.TLTYPE,self.XUSUAN,self.LLMA,self.LLYJ,self.LLLNS,self.LLCKCD,self.QDCD,self.QDMJ,self.QDZX,self.QDZBX,\
    self.QJDL,self.QJTJ,self.QJCFL,self.QJCFL3,self.LDSIMTYPE,self.JSOUT,self.JSINNER,self.JSINONE,self.JSCANZHI,\
    self.YXCANZHI,self.JSNT,self.YXJIEGUO,self.YXXUSUAN,self.GZZONE

    def setzhi(self,lines):
        s = lines.split('=')
        s = s[1].split()
        return s[0]