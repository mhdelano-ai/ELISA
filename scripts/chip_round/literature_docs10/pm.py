import sys, json, urllib.request, urllib.parse, time, xml.etree.ElementTree as ET
B="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def get(u):
    for i in range(4):
        try:
            return urllib.request.urlopen(u, timeout=60).read()
        except Exception as e:
            time.sleep(1.5)
    raise
def search(q, n):
    u=B+"esearch.fcgi?"+urllib.parse.urlencode({"db":"pubmed","term":q,"retmax":n,"retmode":"json","sort":"relevance"})
    return json.loads(get(u))["esearchresult"]["idlist"]
def fetch(ids):
    if not ids: return
    x=get(B+"efetch.fcgi?db=pubmed&retmode=xml&id="+",".join(ids))
    r=ET.fromstring(x)
    for a in r.findall(".//PubmedArticle"):
        pmid=a.findtext(".//PMID")
        t="".join(a.find(".//ArticleTitle").itertext())
        j=a.findtext(".//Journal/ISOAbbreviation") or ""
        y=a.findtext(".//JournalIssue/PubDate/Year") or a.findtext(".//JournalIssue/PubDate/MedlineDate") or ""
        au=a.findall(".//Author")
        fa=(au[0].findtext("LastName") or "") if au else ""
        doi=""
        for i in a.findall("PubmedData/ArticleIdList/ArticleId"):
            if i.get("IdType")=="doi": doi=i.text
        ab=" ".join("".join(e.itertext()) for e in a.findall(".//Abstract/AbstractText"))
        print(f"## PMID {pmid} | {fa} {y} | {j} | doi:{doi}\n{t}\n{ab}\n")
mode=sys.argv[1]
if mode=="s":
    n=int(sys.argv[2])
    for q in sys.argv[3:]:
        ids=search(q,n); print(f"=== Q: {q} -> {ids}"); fetch(ids); time.sleep(0.4)
else:
    fetch(sys.argv[2:])
