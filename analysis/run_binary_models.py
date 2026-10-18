"""Run all four original seven-point nested binary models without published starts."""
import argparse
from pathlib import Path
from nested_logit import fit_model
from prepare_replication import ROOT,load_data

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output-root',type=Path,default=ROOT)
    a=p.parse_args();_,frame=load_data()
    for mid,y in [('M2','actrefoutbin'),('M3','actrefrecbin')]:
        fit_model(frame,y,mid,a.output_root)
        fit_model(frame,y,mid+'_null',a.output_root,null=True)
