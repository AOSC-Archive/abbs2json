#!/usr/bin/env python3

import shlex,re
import sys,os

class AbbsPkg:
    def __init__(self,tree='example',pkgname=''):
        self.pkgname=pkgname
        self.dir=os.path.join(tree,pkgname)
    def file(self,filename):
        return open(os.path.join(self.dir,filename),'r')
    def parse(self,filename):
        def replace_vars(s,d):
            subs=re.findall(r'\$\{.*?\}',s)
            for i in subs:
                varname=i[2,-2]
                s=s.replace(i,d.get(varname,i))
            subs=re.findall(r'\$\w+',s)
            for i in subs:
                varname=i[1:]
                s=s.replace(i,d.get(varname,i))
            return s
        lex=shlex.shlex(instream=self.file(filename),posix=True)
        lex.wordchars+='.'
        lex.whitespace='\t '
        variables={}
        line=[]
        for i in lex:
            if i not in ['\r','\n']:
                line.append(i)
            else:
                if len(line)==0: continue
                variables[line[0]]=replace_vars(''.join(line[2:]),variables)
                line=[]
        return variables


print(AbbsPkg(pkgname='keepassx').parse('spec'))
print(AbbsPkg(pkgname='keepassx').parse('autobuild/defines'))

