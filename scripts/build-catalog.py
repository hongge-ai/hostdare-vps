#!/usr/bin/env python3
"""Build a comparable snapshot from the existing provider pages and raw snapshots.
The input dates belong to those snapshots; this script does not verify live data.
"""
from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib
P=Path('public'); catalog=[]
def num(s):
 m=re.search(r'(\d+(?:\.\d+)?)',str(s));return float(m.group(1)) if m else None
def size(s):
 n=num(s);return n/1024 if n is not None and re.search(r'\bMB\b',s,re.I) else n
def line(s):
 s=s.upper()
 if 'CN2 GIA' in s or 'CN2-GIA' in s:return 'CN2 GIA（名称标称）'
 if 'CN2' in s:return 'CN2（名称标称）'
 if 'CHINA OPTIMIZED' in s:return 'China Optimized（名称标称）'
 if 'DUAL ISP DIA' in s:return 'Dual ISP DIA（名称标称）'
 return '未注明'
def add(**kw):
 defaults=dict(cpu_model=None,cores=None,memory_gb=None,storage=None,bandwidth=None,traffic=None,country=None,city=None,locations=None,network='未注明',system=None,prices=[],renewal='未知',eligibility='未知',stock='未知',currency='USD',source_url=None,verified_at=None,url=None,terms='未知')
 defaults.update(kw);assert defaults['id'] and defaults['provider'] and defaults['source_url'];catalog.append(defaults)
for x in json.loads((P/'compare-assets/plans.json').read_text()):
 add(id='hostdare:'+x['id'],name=x['id'],provider='HostDare',group=x['group'],country=x.get('country'),city=x.get('city'),cpu_model='AMD EPYC' if 'AMD EPYC' in x['cpu'].upper() else None,cores=x.get('cores'),memory_gb=size(x['memory']),storage=x['storage'],bandwidth=x['bandwidth'],traffic=x['traffic'],network=line(x['group']),system=x.get('system'),prices=x['prices'],source_url='hostdare-plans/',verified_at='2026-11-08',url=x['url'],terms='快照标价不含税费及优惠；续费请核对商家页面。')
class TableParser(HTMLParser):
 def __init__(self):super().__init__();self.table=False;self.row=None;self.cell=None;self.rows=[]
 def handle_starttag(self,t,a):
  if t=='table':self.table=True
  if self.table and t=='tr':self.row=[]
  if self.row is not None and t in ('td','th'):self.cell={'text':'','href':[]}
  if self.cell is not None and t=='a':self.cell['href'].append(dict(a).get('href'))
  if self.cell is not None and t=='br':self.cell['text']+=' '
 def handle_data(self,d):
  if self.cell is not None:self.cell['text']+=d
 def handle_endtag(self,t):
  if self.cell is not None and t in ('td','th'):self.row.append(self.cell);self.cell=None
  if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
  if t=='table':self.table=False
for provider,slug in [('RackNerd','racknerd-vps'),('BandwagonHost','bandwagon-vps')]:
 p=TableParser();p.feed((P/slug/'index.html').read_text())
 for row in p.rows[1:]:
  if len(row)<8:continue
  v=[x['text'].strip() for x in row]; href=row[-1]['href'];
  if not href:continue
  prices=[{'period':period,'amount':float(amount)} for period,amount in re.findall(r'(月付|季付|半年付|年付|两年付|三年付)\s*\$([\d.]+)',v[6])]
  if not prices:continue
  locations=v[7] if provider=='BandwagonHost' else '机房以订单页面为准'
  name=v[0];key=hashlib.sha256(href[0].encode()).hexdigest()[:12]
  add(id=slug+':'+key,name=name,provider=provider,group='标准 KVM' if provider=='RackNerd' else 'KVM VPS',cores=num(v[1]),memory_gb=size(v[2]),storage=v[3],traffic=v[4],bandwidth=v[5],locations=locations,network=line(name) if provider=='BandwagonHost' else '未注明',prices=prices,url=href[0],source_url=slug+'/',verified_at='2026-11-08',terms='快照标价不含税费及优惠；具体机房、线路和续费请核对商家页面。')
for x in json.loads((P/'raksmart-vps/plans.json').read_text()):
 if 'VPS' not in x['product']:continue
 opts=dict(x['options']);spec=opts.get('规格','');mc=re.search(r'(\d+)\s*Core',spec,re.I);mm=re.search(r',\s*(\d+(?:\.\d+)?)\s*G',spec,re.I)
 period={'月':'月付','年':'年付'}.get(x['period']);
 if not period:continue
 eligible={'限时秒杀':'每日库存和购买数量有限，具体资格以活动页为准。','年付福利':'年付活动条件及优惠叠加限制以活动页为准。','双ISP DIA上新福利':'可能需要领取优惠券，活动规则以商家页面为准。','精品CN2特惠':'可能需要领取优惠券，活动规则以商家页面为准。'}.get(x['category'],'资格与优惠条件以商家页面为准。')
 key=hashlib.sha256((x['sample']+'|'+x['activity']).encode()).hexdigest()[:12]
 add(id='raksmart:'+key,name=x['name'],provider='Raksmart',group=x['category']+' / '+x['group'],cores=int(mc.group(1)) if mc else None,memory_gb=float(mm.group(1)) if mm else None,storage=opts.get('系统盘'),traffic=opts.get('流量'),network=line(x['name']),system=opts.get('IP数量'),prices=[{'amount':float(x['price']),'period':period}],renewal='$'+x['renewal']+' / '+period+'（该默认配置快照）' if x.get('renewal') else '未知',eligibility=eligible,url=x['url'],source_url='raksmart-vps/',verified_at='2026-11-11',terms='活动页默认配置快照，切换配置或周期后价格可能变化；实际金额及优惠资格以结账页为准。')
ids=[x['id'] for x in catalog];assert len(ids)==len(set(ids)), 'duplicate IDs'
(P/'compare-assets/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
from collections import Counter
print(len(catalog),Counter(x['provider'] for x in catalog))
