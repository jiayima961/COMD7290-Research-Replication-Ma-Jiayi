"""Use native Word conversion plus the packaged document PNG renderer on Windows.

Bundled LibreOffice is unavailable on Windows. This uses a hidden separate Word
automation object and never opens or alters the user's existing document files.
It replaces only the renderer's conversion hook, preserving its canonical
OOXML checks, PDF rasterizer and page image handling. No desktop LibreOffice.
"""
from pathlib import Path
import importlib.util,os,subprocess,sys,shutil,tempfile
ROOT=Path(__file__).resolve().parents[1]
SKILL=Path(r'E:\Codex\plugins\cache\openai-primary-runtime\documents\26.1015.12040\skills\documents')
RUNTIME=Path(r'C:\Users\86150\.cache\codex-runtimes\codex-primary-runtime\dependencies')
def main():
 scratch=(ROOT/'tmp/skill3_docx_qa/scratch').resolve()
 assert scratch.is_relative_to(ROOT.resolve())
 scratch.mkdir(parents=True,exist_ok=True)
 tempfile.tempdir=str(scratch)
 os.environ['PATH']=str(RUNTIME/'native/poppler/Library/bin')+os.pathsep+str(RUNTIME/'native/poppler/bin')+os.pathsep+os.environ['PATH']
 spec=importlib.util.spec_from_file_location('packaged_document_renderer',SKILL/'render_docx.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
 def convert(doc_path,user_profile,convert_tmp_dir,stem,verbose):
  pdf=str(Path(convert_tmp_dir)/(stem+'.pdf'))
  if '--use-existing-exports' in sys.argv:
   saved=ROOT/'tmp/skill3_docx_qa'/stem/(stem+'.pdf')
   if saved.stat().st_mtime < Path(doc_path).stat().st_mtime:
    raise RuntimeError('Word PDF is older than DOCX; export current document again.')
   shutil.copy2(saved,pdf)
   return pdf,'Native Word PDF already exported from the latest DOCX'
  command=['rtk','proxy','powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/word_export_pdf.ps1'),'-InputDocument',doc_path,'-OutputPdf',pdf]
  result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace')
  log=f'Native Word export returncode {result.returncode}\n{result.stdout}\n{result.stderr}'
  if result.returncode!=0:raise RuntimeError(log)
  return pdf,log
 renderer.convert_to_pdf=convert
 for name in ['01_results_comparison','02_python_stata_equivalence']:
  src=ROOT/'report/verification'/f'{name}.docx';dest=ROOT/'tmp/skill3_docx_qa/final'/name
  renderer.rasterize(str(src),str(dest),120,True,True)
  print('Rendered',name,flush=True)
if __name__=='__main__':main()
