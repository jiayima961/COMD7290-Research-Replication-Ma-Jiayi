"""Bind the preserved cached excerpt and the actually reviewed final Word render.

This records the primary agent's completed visual review, not an automated claim
that image hashes can detect layout problems. It never changes research results.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    now = datetime.now(timezone.utc).isoformat()
    source = ROOT / 'records/source_access/ordinal_appendix_cached_excerpt.txt'
    retrieval = {
        'recorded_utc': now,
        'access_date': '2026-10-19',
        'source_url': 'https://medcon-doc.github.io/documentation/content-analysis/additional-analyses/civility-outrage_paper/',
        'method': 'Web tool open returned cached extracted primary page; numerical table at line 6.',
        'crawler_age_reported': 'Approximately two years; exact original retrieval timestamp not supplied.',
        'live_access': 'Direct requests with and without trailing slash returned 404.',
        'preserved_excerpt': source.relative_to(ROOT).as_posix(),
        'excerpt_sha256': sha(source),
        'quantity_count': 75,
        'original_http_body_sha256': None,
        'limitation': 'This hash binds the preserved transcription, not unavailable original HTML. Source targets never enter model estimation.',
        'independent_check': 'records/skill_tests/verify-and-package/independent_source_audit.md',
    }
    (source.parent / 'retrieval_metadata.json').write_text(json.dumps(retrieval, indent=2)+'\n', encoding='utf-8')
    documents=[]
    for stem, pages in [('01_results_comparison',9),('02_python_stata_equivalence',5)]:
        doc=ROOT/'report/verification'/f'{stem}.docx'
        render=ROOT/'tmp/skill3_docx_qa/final'/stem
        pdf=render/f'{stem}.pdf'
        images=sorted(render.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
        assert len(images)==pages, (stem,len(images))
        assert pdf.stat().st_mtime >= doc.stat().st_mtime
        documents.append({
            'path':doc.relative_to(ROOT).as_posix(), 'sha256':sha(doc),
            'source_markdown_sha256':sha(doc.with_suffix('.md')),
            'page_count':pages,
            'qa_pdf_sha256':sha(pdf),
            'reviewed_images':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in images],
            'visual_review':'All final page images opened and inspected by primary agent after the latest render. No clipping, overlap, missing glyphs, orphan table headers or broken rows observed.',
            'outcome':'passed',
        })
    qa={
        'recorded_utc':now,
        'render_command':'Bundled Python tools/render_verification_documents.py --use-existing-exports',
        'renderer':'Packaged documents/render_docx.py rasterizer at 120 dpi, with native Word PDF conversion hook.',
        'conversion':'Hidden separate Microsoft Word automation; bundled LibreOffice unavailable on this Windows runtime. No desktop LibreOffice used.',
        'review_method':'Manual visual inspection of every latest page image, not text extraction alone.',
        'corrections_before_final_review':['Removed inherited title theme color/border.','Kept table header with first data row.','Corrected predictor/grouping wording and regenerated/re-exported both documents.'],
        'documents':documents,
        'all_pages_passed':True,
        'intermediates':'QA PDFs and images stay under excluded tmp; only requested DOCX files are deliverables.',
    }
    dest=ROOT/'records/skill_tests/verify-and-package/document_qa.json'
    dest.write_text(json.dumps(qa,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_excerpt_sha256':sha(source),'reviewed_docx':len(documents),'reviewed_pages':sum(d['page_count'] for d in documents),'layout_passed':True}))

if __name__=='__main__':main()
