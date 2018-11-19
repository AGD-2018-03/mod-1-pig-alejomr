
from __future__ import print_function
from IPython.core.magic import (Magics, 
                                magics_class, 
                                line_magic,
                                cell_magic, 
                                line_cell_magic)
import pexpect
import re

PIGPATH = 'pig -4 log4j.properties -x local '
PIGPROMPT = 'grunt> '
PIGCONT = '>> '

@magics_class
class bdMagic(Magics):

    def __init__(self, shell):
        super(bdMagic, self).__init__(shell)
        self.pig = None
#        self.pig = pexpect.spawn(PIGPATH)
#        self.pig.expect(PROMPT)
#        for line in self.child.before.decode().split('\r\n'):
#            print(line)

    @line_magic
    def pig_init(self, line):
        if self.pig is not None:
            self.pig.close()
        self.pig = pexpect.spawn(PIGPATH, timeout=300)
        self.pig.expect(PIGPROMPT)
        for x in self.pig.before.decode().split('\r\n'):
            print(x)
        return None
            
    @cell_magic
    def pig(self, line, cell):
        if self.pig is None:
            self.pig_init(line)
        x = cell.split('\n')
        for row in x:
            self.pig.sendline(row)
            self.pig.expect(['\r\n'+PIGCONT, '\r\n'+PIGPROMPT])
            for text in self.pig.before.decode().split('\r\n'):
                if text not in x:
                    print(text)
        return None        
        
        
        
__ip = get_ipython()
bdmagic = bdMagic(__ip)
__ip.register_magics(bdmagic)
