import re
import argparse


symbols = {
        r'\\ ' : '',
        r'\\left\s*\|' : r'\\abs(',
        r'\\right\s*\|' : ')',
        r'\\left' : '',
        r'\\right' : '',
        r'\\cdot' : '*',
        r'\\times' : '*',
        r'\\div' : '/',
        ' ' : '',
        '{' : '(',
        '}' : ')',
        '\^' : '**'
        }

ops =  {
        r'\\log' : 'np.log10',
        r'\\ln' : 'np.log',
        r'\\sin' : 'np.sin',
        r'\\cos' : 'np.cos',
        r'\\tan' : 'np.tan',
        r'\\arcsin' : 'np.arcsin',
        r'\\arccos' : 'np.arccos',
        r'\\arctan' : 'np.arctan',
        r'\\sinh' : 'np.sinh',
        r'\\cosh' : 'np.cosh',
        r'\\tanh' : 'np.tanh',
        r'\\sqrt' : 'np.sqrt',
        r'\\exp' : 'np.exp',
        r'\\abs' : 'np.abs'
        }

funs = [r'\\frac', r'\\log_']

consts = {
          r'\\pi' : 'np.pi',
          }

def isint(s):
    if s == '.':
        return True    
    else:
        try: 
            int(s)
            return True
        except ValueError:
            return False


def getCloseBr(s):
    openBr = 0
    for pos, char in enumerate(s):
        if char == '(':
            openBr += 1
        elif char == ')':
            openBr -= 1
        if openBr == 0:
            return pos
            break

     
def repFunctions(f, s):  
    
    if f == r'\\frac':
        
        while True:  
            try:        
                i = [m.start() for m in re.finditer(f, s)][0]
            except:
                break
            s_strip1 = s[i+len(f)-1:]            
            pos1 = getCloseBr(s_strip1)
            s_strip2 = s_strip1[pos1+1:]
            pos2 = getCloseBr(s_strip2)
            s = s[:i] + '(' + s_strip1[:pos1+1] + '/' + s_strip2[:pos2+1] + ')' + s_strip2[pos2+1:]  
                      
    if f == r'\\log_':
        while True:  
            try:        
                i = [m.start() for m in re.finditer(f, s)][0]
            except:
                break
            s_strip = s[i+len(f)-1:]
            
            if s_strip[0] == '(':
                pos1 = getCloseBr(s_strip)
                base = s_strip[:pos1+1]
                pos2 = getCloseBr(s_strip[pos1+1:]) + pos1+1
                arg = s_strip[pos1+1:pos2+1]
                pos = pos2
            else:
                base = s_strip.split('(')[0]
                pos = getCloseBr(s_strip[len(base):]) + len(base)
                arg = s_strip[len(base):pos+1]
            s = s[:i] + '(np.log('+arg+')/np.log('+base+'))' + s_strip[pos+1:]

    return s



def insMultiply(s):
    s_temp = s
    for v in ops.values():
        s_temp = re.sub(v, '('*len(v), s_temp)
    for v in consts.values():
        s_temp = re.sub(v, '('*(len(v)-1)+')', s_temp)
    ops_list = ['*', '/', '(', '+', '-', '_']
    idx_list = []
    for i, char in enumerate(s_temp):
        if char == '(':
            if s_temp[i-1] not in ops_list and i != 0:
                idx_list.append(i)
                
        elif char not in ops_list and char != ')' and i != 0:           
            if isint(char) == False:
                if s_temp[i-1] not in ops_list:
                    idx_list.append(i)
            #elif isint(char) == True:
            #    if s_temp[i-1] not in ops_list and isint(s_temp[i-1]) == False:
            #        idx_list.append(i)
                                  
    idx_list = list(set(idx_list))                                 
    idx_list.sort()
    for c, i in enumerate(idx_list):
        s = s[:i+c] + '*' + s[i+c:]
    return s

def remBrackets(s):
    idx_list = []
    for i, char in enumerate(s):
        if char == '(':
            if s[i-1] in ['+', '-', '/', '*', ')', '(', '_']:
                pos = getCloseBr(s[i:]) + i
                if len([1 for o in ['+', '-', '/', '*', ')', '(', '_'] if o in s[i+1:pos]]) == 0:
                  idx_list.append(i)
                  idx_list.append(pos)
                if s[i+1] == '(':
                    pos2 = getCloseBr(s[i+1:]) + i+1
                    if pos2 == pos - 1:
                        idx_list.append(i+1)
                        idx_list.append(pos2)
                
  
    idx_list = list(set(idx_list))
    idx_list.sort()
    for c, i in enumerate(idx_list):
        s = s[:i-c] + '' + s[i-c + 1:]
    return s            
        
            
def main():
    
    while True:
        
        s = input("Paste your expression: ")
        
        for k, v in symbols.items():
            s = re.sub(k, v, s)            
            
        for k, v in consts.items():
            s = re.sub(k, v, s)
            
        for f in funs:
            s = repFunctions(f, s)  

        for k, v in ops.items():
            s = re.sub(k, v, s)
            

            
        s = insMultiply(s)
        
        s = remBrackets(s)
            
        print("result : " + s)


if __name__ == "__main__":
    main()
