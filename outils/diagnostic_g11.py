"""G11 : réussites, recherches et documents requis trouvés, sur un fichier mesures/p0/*-results.json."""
import json,sys,re,statistics as st
from collections import Counter,defaultdict
d=json.load(open(sys.argv[1]))
tasks={t['id']:t for t in d['tasks']}
t0=next(iter(tasks.values()))
print('task keys',list(t0.keys()))
def req(t):
    for path in [('required_documents',),('user_scenario','required_documents'),('evaluation_criteria','required_documents')]:
        x=t
        try:
            for p in path: x=x[p]
            return x
        except Exception: pass
    s=json.dumps(t); m=re.search(r'"required_documents": (\[[^\]]*\])',s)
    return json.loads(m.group(1)) if m else None
term=Counter(); rows=[]
for s in d['simulations']:
    term[s['termination_reason']]+=1
    ri=s.get('reward_info'); r=ri.get('reward') if ri else None
    msgs=s['messages']
    nsearch=sum(1 for m in msgs if m.get('tool_calls') for c in m['tool_calls'] if c['name']=='KB_search')
    ntools=sum(len(m['tool_calls']) for m in msgs if m.get('tool_calls') and m['role']=='assistant')
    seen=set()
    for m in msgs:
        if m['role']=='tool' and m.get('content'):
            seen|=set(re.findall(r'ID: (\S+)',m['content']))
    rq=req(tasks[s['task_id']]) or []
    rec=len(set(rq)&seen)/len(rq) if rq else None
    rows.append(dict(task=s['task_id'],trial=s['trial'],r=r,term=s['termination_reason'],ns=nsearch,nt=ntools,rec=rec,nreq=len(rq),nmsg=len(msgs)))
print('termination',dict(term))
sc=[x for x in rows if x['r'] is not None and x['term'] in ('user_stop','agent_stop','max_steps','too_many_errors')]
print('all with reward',sum(1 for x in rows if x['r'] is not None),'succ',sum(1 for x in rows if x['r']==1))
by=defaultdict(list)
for x in rows:
    if x['r'] is not None: by[x['term']].append(x['r'])
print({k:(len(v),sum(v)) for k,v in by.items()})
ok=[x for x in rows if x['r'] is not None]
print('N',len(ok),'succ',sum(x['r'] for x in ok),'tasks',len(set(x['task'] for x in ok)))
pt=defaultdict(list)
for x in ok: pt[x['task']].append(x['r'])
print('tasks solved ever',sorted((k,sum(v),len(v)) for k,v in pt.items() if sum(v)>0))
print('searches median',st.median(x['ns'] for x in ok),'mean',round(st.mean(x['ns'] for x in ok),2),'zero',sum(1 for x in ok if x['ns']==0))
print('searches in successes',[x['ns'] for x in ok if x['r']==1])
print('nreq median',st.median(x['nreq'] for x in ok),'mean task-level', round(st.mean(len(req(t) or []) for t in tasks.values()),1), 'over',len(tasks),'tasks')
recs=[x['rec'] for x in ok if x['rec'] is not None]
print('doc recall mean',round(st.mean(recs),3),'median',round(st.median(recs),3))
for lo,hi in [(0.8,1.01),(0.4,0.8),(0,0.4)]:
    g=[x for x in ok if x['rec'] is not None and lo<=x['rec']<hi]
    print(f'rec [{lo},{hi}) succ {sum(x["r"] for x in g)}/{len(g)}')
print('succ rows',[(x['task'],x['nreq'],round(x['rec'],2),x['ns']) for x in ok if x['r']==1])
