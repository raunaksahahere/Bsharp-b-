import sys, re, math

class BSharpError(Exception):
    def __init__(self, msg, line=0):
        self.bsharp_message = msg; self.line = line; super().__init__(msg)
    def friendly(self):
        return f"Error{f' (line {self.line})' if self.line else ''}: {self.bsharp_message}"

class BSharpReturn(Exception):
    def __init__(self, v): self.value = v

KEYWORDS = {
    'let','be','change','to','say','ask','and','store','in','as','if','then','else','end',
    'while','do','for','each','from','define','function','with','return','call','list','of',
    'dictionary','try','catch','use','library','note','not','or','integer','float','boolean',
    'string','true','false','add','remove','get','length','join','read','write','explain',
    'plus','minus','times','divided','by','modulo','is','equal','greater','less','than',
    'at','least','most','does','contain','contains','the'
}

def lex(source):
    tokens = []
    for lineno, line in enumerate(source.splitlines(), 1):
        if line.lstrip().startswith('note'): continue
        pos = 0
        while pos < len(line):
            if line[pos] in ' \t': pos += 1; continue
            if line[pos] == '"':
                end = line.find('"', pos+1)
                if end == -1: raise BSharpError(f'Unclosed string at column {pos+1}', lineno)
                tokens.append(('STRING', line[pos+1:end], lineno)); pos = end+1; continue
            m = re.match(r'\d+\.\d+', line[pos:])
            if m: tokens.append(('FLOAT', float(m.group()), lineno)); pos += len(m.group()); continue
            m = re.match(r'\d+', line[pos:])
            if m: tokens.append(('INTEGER', int(m.group()), lineno)); pos += len(m.group()); continue
            if line[pos] == '[': tokens.append(('LBRACKET','[',lineno)); pos+=1; continue
            if line[pos] == ']': tokens.append(('RBRACKET',']',lineno)); pos+=1; continue
            if line[pos] == ',': tokens.append(('COMMA',',',lineno)); pos+=1; continue
            m = re.match(r'[A-Za-z_][A-Za-z0-9_]*', line[pos:])
            if m:
                w = m.group(); lw = w.lower()
                tokens.append(('KEYWORD' if lw in KEYWORDS else 'IDENTIFIER',
                                lw if lw in KEYWORDS else w, lineno)); pos += len(w); continue
            raise BSharpError(f'Unknown character "{line[pos]}" at column {pos+1}', lineno)
    tokens.append(('EOF', None, 0))
    return tokens

class Parser:
    def __init__(self, tokens): self.t = tokens; self.pos = 0
    def cur(self): return self.t[min(self.pos, len(self.t)-1)]
    def adv(self):
        t = self.t[self.pos]
        if self.pos < len(self.t)-1: self.pos += 1
        return t
    def ln(self): return self.cur()[2]
    def iskw(self, *w): return self.cur()[0]=='KEYWORD' and self.cur()[1] in w
    def exkw(self, *w):
        t = self.cur()
        if t[0]=='KEYWORD' and t[1] in w: return self.adv()
        raise BSharpError(f'Expected "{" or ".join(w)}" but got "{t[1]}"', t[2])
    def exid(self):
        t = self.cur()
        if t[0]=='IDENTIFIER': self.adv(); return t[1]
        raise BSharpError(f'Expected a variable name but got "{t[1]}"', t[2])
    def nd(self, k, ln=None, **kw): return {'kind':k,'line':ln if ln is not None else self.ln(),**kw}

    def parse(self):
        s = []
        while self.cur()[0] != 'EOF':
            st = self.stmt()
            if st: s.append(st)
        return self.nd('Program', 0, statements=s)

    def block(self, stop=('end',)):
        s = []
        while self.cur()[0] != 'EOF':
            if self.cur()[0]=='KEYWORD' and self.cur()[1] in stop: break
            st = self.stmt()
            if st: s.append(st)
        return s

    def stmt(self):
        t = self.cur(); ln = t[2]
        if t[0] == 'EOF': return None
        if t[0] == 'KEYWORD':
            k = t[1]
            if k == 'note':
                cl = ln
                while self.cur()[2]==cl and self.cur()[0]!='EOF': self.adv()
                return None
            if k == 'let':     return self.p_let()
            if k == 'change':  return self.p_change()
            if k == 'say':     return self.p_say()
            if k == 'ask':     return self.p_ask()
            if k == 'if':      return self.p_if()
            if k == 'while':   return self.p_while()
            if k == 'for':     return self.p_for()
            if k == 'define':  return self.p_def()
            if k == 'return':  return self.p_return()
            if k == 'call':    return self.nd('CallStmt', ln, call=self.p_callexpr())
            if k == 'try':     return self.p_try()
            if k == 'use':     return self.p_use()
            if k == 'add':     return self.p_add()
            if k == 'remove':  return self.p_remove()
            if k == 'read':    return self.p_read()
            if k == 'write':   return self.p_write()
            if k == 'explain': self.adv(); return self.nd('Explain', ln)
        raise BSharpError(f'Did not understand line starting with "{t[1]}"', ln)

    def p_let(self):
        ln=self.ln(); self.exkw('let'); name=self.exid(); self.exkw('be')
        th=None
        if self.iskw('integer','float','boolean','string'): th=self.adv()[1]
        if self.iskw('list'):
            self.adv(); self.exkw('of')
            return self.nd('Let',ln,name=name,th='list',value=self.nd('LL',ln,items=self.p_csv()))
        if self.iskw('dictionary'):
            self.adv(); self.exkw('with'); pairs=[]
            while not self.iskw('end') and self.cur()[0]!='EOF':
                key=self.exid(); self.exkw('as'); val=self.p_expr(); pairs.append((key,val))
            self.exkw('end')
            return self.nd('Let',ln,name=name,th='dict',value=self.nd('DL',ln,pairs=pairs))
        if self.iskw('call'):  return self.nd('Let',ln,name=name,th=th,value=self.p_callexpr())
        if self.iskw('get'):   return self.nd('Let',ln,name=name,th=th,value=self.p_get())
        if self.iskw('join'):  return self.nd('Let',ln,name=name,th=th,value=self.p_join())
        return self.nd('Let',ln,name=name,th=th,value=self.p_expr())

    def p_change(self):
        ln=self.ln(); self.exkw('change'); name=self.exid(); self.exkw('to')
        if self.iskw('call'):  return self.nd('Change',ln,name=name,value=self.p_callexpr())
        if self.iskw('get'):   return self.nd('Change',ln,name=name,value=self.p_get())
        if self.iskw('join'):  return self.nd('Change',ln,name=name,value=self.p_join())
        return self.nd('Change',ln,name=name,value=self.p_expr())

    def p_say(self):
        ln=self.ln(); self.exkw('say')
        return self.nd('Say',ln,items=self.p_csv())

    def p_ask(self):
        ln=self.ln(); self.exkw('ask'); prompt=self.p_primary(); th=None
        if self.iskw('as'):
            self.adv()
            if self.iskw('integer','float','boolean','string'): th=self.adv()[1]
        self.exkw('and'); self.exkw('store'); self.exkw('in')
        return self.nd('Ask',ln,prompt=prompt,th=th,variable=self.exid())

    def p_if(self):
        ln=self.ln(); self.exkw('if'); cond=self.p_cond(); self.exkw('then')
        body=self.block(('end','else')); elseifs=[]; else_body=None
        while self.iskw('else'):
            self.adv()
            if self.iskw('if'):
                self.adv(); ec=self.p_cond(); self.exkw('then')
                elseifs.append((ec, self.block(('end','else'))))
            else: else_body=self.block(('end',)); break
        self.exkw('end')
        return self.nd('If',ln,cond=cond,body=body,elseifs=elseifs,else_body=else_body)

    def p_while(self):
        ln=self.ln(); self.exkw('while'); cond=self.p_cond(); self.exkw('do')
        body=self.block(); self.exkw('end')
        return self.nd('While',ln,cond=cond,body=body)

    def p_for(self):
        ln=self.ln(); self.exkw('for'); self.exkw('each'); var=self.exid()
        if self.iskw('from'):
            self.adv(); start=self.p_expr(); self.exkw('to'); end=self.p_expr()
            self.exkw('do'); body=self.block(); self.exkw('end')
            return self.nd('ForRange',ln,var=var,start=start,end=end,body=body)
        self.exkw('in'); it=self.p_expr(); self.exkw('do')
        body=self.block(); self.exkw('end')
        return self.nd('ForEach',ln,var=var,iterable=it,body=body)

    def p_def(self):
        ln=self.ln(); self.exkw('define'); self.exkw('function'); name=self.exid(); params=[]
        if self.iskw('with'):
            self.adv(); params.append(self.exid())
            while self.iskw('and'): self.adv(); params.append(self.exid())
        self.exkw('do'); body=self.block(); self.exkw('end')
        return self.nd('FuncDef',ln,name=name,params=params,body=body)

    def p_return(self):
        ln=self.ln(); self.exkw('return')
        if self.cur()[0]=='EOF': return self.nd('Return',ln,value=None)
        return self.nd('Return',ln,value=self.p_expr())

    def p_callexpr(self):
        ln=self.ln(); self.exkw('call'); name=self.exid(); args=[]
        if self.iskw('with'):
            self.adv(); args.append(self.p_expr())
            while self.iskw('and'): self.adv(); args.append(self.p_expr())
        return self.nd('CallExpr',ln,name=name,args=args)

    def p_try(self):
        ln=self.ln(); self.exkw('try'); tb=self.block(('catch',)); self.exkw('catch')
        ev=self.exid(); cb=self.block(); self.exkw('end')
        return self.nd('TryCatch',ln,try_body=tb,err_var=ev,catch_body=cb)

    def p_use(self):
        ln=self.ln(); self.exkw('use'); self.exkw('library')
        return self.nd('UseLib',ln,name=self.exid())

    def p_add(self):
        ln=self.ln(); self.exkw('add'); value=self.p_expr(); self.exkw('to')
        return self.nd('AddList',ln,value=value,lst=self.exid())

    def p_remove(self):
        ln=self.ln(); self.exkw('remove'); value=self.p_expr(); self.exkw('from')
        return self.nd('RemList',ln,value=value,lst=self.exid())

    def p_read(self):
        ln=self.ln(); self.exkw('read'); self.exkw('from'); fn=self.p_primary()
        self.exkw('and'); self.exkw('store'); self.exkw('in')
        return self.nd('ReadFile',ln,filename=fn,var=self.exid())

    def p_write(self):
        ln=self.ln(); self.exkw('write'); value=self.p_expr(); self.exkw('to')
        return self.nd('WriteFile',ln,value=value,filename=self.p_primary())

    def p_get(self):
        ln=self.ln(); self.exkw('get'); self.exkw('length'); self.exkw('of')
        return self.nd('GetLen',ln,target=self.p_primary())

    def p_join(self):
        ln=self.ln(); self.exkw('join'); target=self.p_primary(); self.exkw('with')
        return self.nd('JoinStr',ln,target=target,sep=self.p_primary())

    def p_csv(self):
        if self.cur()[0]=='EOF' or self.iskw('end','then','do','else'): return []
        items=[self.p_expr()]
        while self.cur()[0]=='COMMA': self.adv(); items.append(self.p_expr())
        return items

    def p_cond(self):
        left=self.p_cmp()
        while self.iskw('and','or'):
            op=self.adv()[1]; right=self.p_cmp()
            left=self.nd('Logic',left['line'],op=op,left=left,right=right)
        return left

    def p_cmp(self):
        ln=self.ln()
        if self.iskw('not'): self.adv(); return self.nd('NotOp',ln,operand=self.p_cmp())
        left=self.p_expr()
        if self.iskw('is'):
            self.adv()
            if self.iskw('not'):    self.adv(); self.exkw('equal'); self.exkw('to'); return self.nd('Cmp',ln,op='!=',left=left,right=self.p_expr())
            if self.iskw('equal'):  self.adv(); self.exkw('to');    return self.nd('Cmp',ln,op='==',left=left,right=self.p_expr())
            if self.iskw('greater'):self.adv(); self.exkw('than');  return self.nd('Cmp',ln,op='>',left=left,right=self.p_expr())
            if self.iskw('less'):   self.adv(); self.exkw('than');  return self.nd('Cmp',ln,op='<',left=left,right=self.p_expr())
            if self.iskw('at'):
                self.adv(); q=self.adv()[1]
                return self.nd('Cmp',ln,op='>=' if q=='least' else '<=',left=left,right=self.p_expr())
            raise BSharpError('After "is" expected: "equal to", "not equal to", "greater/less than", "at least/most"', ln)
        if self.iskw('does'):
            self.adv(); neg=self.iskw('not')
            if neg: self.adv()
            if self.iskw('contain','contains'):
                self.adv(); return self.nd('Cmp',ln,op='notin' if neg else 'in',left=left,right=self.p_expr())
        return left

    def p_expr(self):
        left=self.p_primary()
        while self.iskw('plus','minus','times','divided','modulo'):
            op=self.adv()[1]
            if op=='divided': self.exkw('by'); op='/'
            elif op=='times':  op='*'
            elif op=='plus':   op='+'
            elif op=='minus':  op='-'
            elif op=='modulo': op='%'
            right=self.p_primary()
            left=self.nd('BinOp',left['line'],op=op,left=left,right=right)
        return left

    def p_primary(self):
        t=self.cur(); ln=t[2]
        if t[0]=='INTEGER': self.adv(); return self.nd('Num',ln,value=t[1])
        if t[0]=='FLOAT':   self.adv(); return self.nd('Num',ln,value=t[1])
        if t[0]=='STRING':  self.adv(); return self.nd('Str',ln,value=t[1])
        if t[0]=='KEYWORD' and t[1]=='true':  self.adv(); return self.nd('Bool',ln,value=True)
        if t[0]=='KEYWORD' and t[1]=='false': self.adv(); return self.nd('Bool',ln,value=False)
        if t[0]=='LBRACKET':
            self.adv(); items=[]
            while self.cur()[0]!='RBRACKET' and self.cur()[0]!='EOF':
                items.append(self.p_expr())
                if self.cur()[0]=='COMMA': self.adv()
            if self.cur()[0]=='RBRACKET': self.adv()
            return self.nd('LL',ln,items=items)
        if t[0]=='KEYWORD' and t[1]=='call': return self.p_callexpr()
        if t[0]=='KEYWORD' and t[1]=='get':  return self.p_get()
        if t[0]=='KEYWORD' and t[1]=='join': return self.p_join()
        if t[0]=='IDENTIFIER': self.adv(); return self.nd('Var',ln,name=t[1])
        raise BSharpError(f'Expected a value (number, text, variable, true/false) but got "{t[1]}"', ln)


class Env:
    def __init__(self, parent=None): self.vars={}; self.parent=parent
    def get(self, name, line=0):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name, line)
        raise BSharpError(f'Variable "{name}" not found. Create it with "let {name} be ..."', line)
    def set(self, name, v): self.vars[name]=v
    def update(self, name, v, line=0):
        if name in self.vars: self.vars[name]=v; return
        if self.parent: self.parent.update(name,v,line); return
        raise BSharpError(f'Cannot change "{name}" — create it first with "let {name} be ..."', line)


class Runtime:
    def __init__(self, trace=False, src=None):
        self.ge=Env(); self.libs=set(); self.trace=trace; self.src=src or []; self.last_op=None

    def run(self, prog): self.blk(prog['statements'], self.ge)
    def blk(self, ss, env):
        for s in ss:
            if s: self.ex(s, env)

    def ex(self, s, env):
        k=s['kind']; ln=s.get('line',0)
        if self.trace:
            src=self.src[ln-1].strip() if ln and ln<=len(self.src) else ''
            print(f'  [trace {ln:3d}] {src}')

        if k=='Let':
            v=self.ev(s['value'],env); v=self.coerce(v,s.get('th'),ln)
            env.set(s['name'],v); self.last_op=f'Created "{s["name"]}" = {self.desc(v)}'
        elif k=='Change':
            v=self.ev(s['value'],env); env.update(s['name'],v,ln)
            self.last_op=f'Changed "{s["name"]}" → {self.desc(v)}'
        elif k=='Say':
            out=' '.join(self.tostr(self.ev(i,env)) for i in s['items'])
            print(out); self.last_op=f'Printed: {out}'
        elif k=='Ask':
            pr=self.tostr(self.ev(s['prompt'],env)); raw=input(pr+' ')
            th=s.get('th')
            if th=='integer':
                try: raw=int(raw)
                except: raise BSharpError(f'Expected integer, got "{raw}"', ln)
            elif th=='float':
                try: raw=float(raw)
                except: raise BSharpError(f'Expected number, got "{raw}"', ln)
            elif th=='boolean':
                if raw.lower() in ('true','yes','1'): raw=True
                elif raw.lower() in ('false','no','0'): raw=False
                else: raise BSharpError(f'Expected true/false, got "{raw}"', ln)
            env.set(s['variable'],raw); self.last_op=f'Read input → "{s["variable"]}"'
        elif k=='If':
            if self.truthy(self.ev(s['cond'],env)): self.blk(s['body'],Env(env)); return
            for ec,eb in s.get('elseifs',[]):
                if self.truthy(self.ev(ec,env)): self.blk(eb,Env(env)); return
            if s.get('else_body'): self.blk(s['else_body'],Env(env))
        elif k=='While':
            i=0
            while self.truthy(self.ev(s['cond'],env)):
                self.blk(s['body'],Env(env)); i+=1
                if i>100000: raise BSharpError(
                    'Loop ran over 100,000 times — possible infinite loop. Check your condition.', ln)
        elif k=='ForRange':
            for i in range(int(self.ev(s['start'],env)), int(self.ev(s['end'],env))+1):
                c=Env(env); c.set(s['var'],i); self.blk(s['body'],c)
        elif k=='ForEach':
            it=self.ev(s['iterable'],env)
            items=(it if isinstance(it,list) else list(it.keys()) if isinstance(it,dict)
                   else list(it) if isinstance(it,str)
                   else (_ for _ in ()).throw(BSharpError(f'Cannot iterate {self.desc(it)}',ln)))
            for item in items:
                c=Env(env); c.set(s['var'],item); self.blk(s['body'],c)
        elif k=='FuncDef':
            env.set(s['name'],{'__func__':True,'params':s['params'],'body':s['body'],'cl':env})
            self.last_op=f'Defined function "{s["name"]}"'
        elif k=='Return': raise BSharpReturn(self.ev(s['value'],env) if s.get('value') else None)
        elif k=='CallStmt': self.call(s['call'],env)
        elif k=='TryCatch':
            try: self.blk(s['try_body'],Env(env))
            except BSharpError as e:
                ce=Env(env); ce.set(s['err_var'],e.bsharp_message); self.blk(s['catch_body'],ce)
        elif k=='UseLib': self.libs.add(s['name']); self.last_op=f'Loaded library "{s["name"]}"'
        elif k=='AddList':
            v=self.ev(s['value'],env); lst=env.get(s['lst'],ln)
            if not isinstance(lst,list): raise BSharpError(f'"{s["lst"]}" is not a list',ln)
            lst.append(v); self.last_op=f'Added {self.desc(v)} to "{s["lst"]}" ({len(lst)} items)'
        elif k=='RemList':
            v=self.ev(s['value'],env); lst=env.get(s['lst'],ln)
            if not isinstance(lst,list): raise BSharpError(f'"{s["lst"]}" is not a list',ln)
            if v not in lst: raise BSharpError(f'{self.desc(v)} not found in "{s["lst"]}"',ln)
            lst.remove(v); self.last_op=f'Removed {self.desc(v)} from "{s["lst"]}"'
        elif k=='ReadFile':
            fn=self.tostr(self.ev(s['filename'],env))
            try:
                with open(fn,'r',encoding='utf-8') as f: content=f.read()
            except FileNotFoundError: raise BSharpError(f'File "{fn}" not found',ln)
            except PermissionError:   raise BSharpError(f'Permission denied: "{fn}"',ln)
            env.set(s['var'],content); self.last_op=f'Read {len(content)} chars from "{fn}"'
        elif k=='WriteFile':
            v=self.tostr(self.ev(s['value'],env)); fn=self.tostr(self.ev(s['filename'],env))
            with open(fn,'w',encoding='utf-8') as f: f.write(v)
            self.last_op=f'Wrote {len(v)} chars to "{fn}"'
        elif k=='Explain':
            print(f'[explain] {self.last_op or "No operation has been performed yet."}')
        else:
            raise BSharpError(f'Unknown statement: {k}', ln)

    def call(self, c, env):
        name=c['name']; ln=c.get('line',0)
        fn=env.get(name,ln)
        if not isinstance(fn,dict) or not fn.get('__func__'):
            raise BSharpError(f'"{name}" is not a function — make sure you defined it with "define function {name} ..."', ln)
        args=[self.ev(a,env) for a in c['args']]
        if len(args)!=len(fn['params']):
            raise BSharpError(f'"{name}" expects {len(fn["params"])} arg(s), got {len(args)}', ln)
        ce=Env(fn['cl'])
        for p,v in zip(fn['params'],args): ce.set(p,v)
        try: self.blk(fn['body'],ce); return None
        except BSharpReturn as r:
            self.last_op=f'Called "{name}" → {self.desc(r.value)}'; return r.value

    def ev(self, x, env):
        if x is None: return None
        k=x['kind']; ln=x.get('line',0)
        if k=='Num':  return x['value']
        if k=='Str':  return x['value']
        if k=='Bool': return x['value']
        if k=='Var':  return env.get(x['name'],ln)
        if k=='LL':   return [self.ev(i,env) for i in x['items']]
        if k=='DL':   return {p[0]:self.ev(p[1],env) for p in x['pairs']}
        if k=='BinOp':
            l=self.ev(x['left'],env); r=self.ev(x['right'],env); op=x['op']
            if op=='+': return (str(l)+str(r)) if isinstance(l,str) or isinstance(r,str) else l+r
            if op=='-': return l-r
            if op=='*': return l*r
            if op=='/':
                if r==0: raise BSharpError('Cannot divide by zero.',ln)
                res=l/r; return int(res) if res==int(res) else res
            if op=='%':
                if r==0: raise BSharpError('Cannot compute remainder when dividing by zero.',ln)
                return l%r
        if k=='Cmp':
            l=self.ev(x['left'],env); r=self.ev(x['right'],env); op=x['op']
            if op=='==':    return l==r
            if op=='!=':    return l!=r
            if op=='>':     return l>r
            if op=='<':     return l<r
            if op=='>=':    return l>=r
            if op=='<=':    return l<=r
            if op=='in':    return l in r
            if op=='notin': return l not in r
        if k=='Logic':
            l=self.truthy(self.ev(x['left'],env))
            if x['op']=='and': return l and self.truthy(self.ev(x['right'],env))
            return l or self.truthy(self.ev(x['right'],env))
        if k=='NotOp': return not self.truthy(self.ev(x['operand'],env))
        if k=='GetLen':
            t=self.ev(x['target'],env)
            if hasattr(t,'__len__'): return len(t)
            raise BSharpError(f'Cannot get length of {self.desc(t)}',ln)
        if k=='JoinStr':
            t=self.ev(x['target'],env); sep=self.tostr(self.ev(x['sep'],env))
            if not isinstance(t,list): raise BSharpError(f'join needs a list, got {self.desc(t)}',ln)
            return sep.join(self.tostr(i) for i in t)
        if k=='CallExpr':
            r=self.call(x,env); self.last_op=f'Called "{x["name"]}" → {self.desc(r)}'; return r
        raise BSharpError(f'Unknown expression: {k}', ln)

    def coerce(self, v, th, ln):
        if not th or th in ('list','dict'): return v
        if th=='integer':
            try: return int(v)
            except: raise BSharpError(f'Cannot convert {self.desc(v)} to integer', ln)
        if th=='float':
            try: return float(v)
            except: raise BSharpError(f'Cannot convert {self.desc(v)} to float', ln)
        if th=='string': return self.tostr(v)
        if th=='boolean':
            if isinstance(v,bool): return v
            if str(v).lower() in ('true','yes','1'): return True
            if str(v).lower() in ('false','no','0'): return False
            raise BSharpError(f'Cannot convert {self.desc(v)} to boolean', ln)
        return v

    def truthy(self, v):
        if v is None: return False
        if isinstance(v,bool): return v
        if isinstance(v,(int,float)): return v!=0
        if isinstance(v,(str,list,dict)): return len(v)>0
        return True

    def tostr(self, v):
        if v is None: return ''
        if isinstance(v,bool): return 'true' if v else 'false'
        if isinstance(v,float): return str(int(v)) if v==int(v) else str(v)
        if isinstance(v,list): return '['+', '.join(self.tostr(i) for i in v)+']'
        if isinstance(v,dict) and not v.get('__func__'):
            return '{'+', '.join(f'{k}: {self.tostr(val)}' for k,val in v.items())+'}'
        return str(v)

    def desc(self, v):
        if v is None: return 'nothing'
        if isinstance(v,bool): return f'boolean {"true" if v else "false"}'
        if isinstance(v,int): return f'integer {v}'
        if isinstance(v,float): return f'decimal {v}'
        if isinstance(v,str): return f'text "{v}"'
        if isinstance(v,list): return f'list({len(v)} items)'
        if isinstance(v,dict): return 'a function' if v.get('__func__') else f'dictionary({len(v)} keys)'
        return str(type(v).__name__)


HELP = """
B# (B-sharp) Programming Language v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usage:
  python bsharp.py <file.bsharp>            Run a program
  python bsharp.py <file.bsharp> --trace    Run with step-by-step trace
  python bsharp.py --help                   Show this help
"""

def main():
    args=sys.argv[1:]
    if not args or '--help' in args or '-h' in args: print(HELP); return
    fname=next((a for a in args if not a.startswith('--')), None)
    trace='--trace' in args
    if not fname: print('Error: provide a .bsharp file'); sys.exit(1)
    try:
        with open(fname,'r',encoding='utf-8') as f: source=f.read()
    except FileNotFoundError: print(f'Error: File "{fname}" not found.'); sys.exit(1)
    sl=source.splitlines()
    if trace: print(f'[trace] Running "{fname}" — {len(sl)} lines\n{"─"*50}')
    try:
        tokens=lex(source); prog=Parser(tokens).parse(); Runtime(trace=trace,src=sl).run(prog)
    except BSharpError as e:
        print(f'\n{"━"*50}\n{e.friendly()}\n{"━"*50}'); sys.exit(1)
    except KeyboardInterrupt: print('\n[stopped]'); sys.exit(0)

if __name__=='__main__': main()