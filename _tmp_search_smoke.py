"""302.AI 多源搜索冒烟测试：跑全部 9 个 provider，验证 search() 和 search_then_ask()。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
import geolib  # noqa
import sample as S  # noqa
import urllib3
urllib3.disable_warnings()

# 9 个 provider，每个一个简单查询
tests = [
    ("tavily",         "GeoLook GEO tool",                       "全球 - tavily"),
    ("bocha",          "GeoLook 地理信息工具",                    "中文 - bocha"),
    ("unifuncs",       "AI 工具评测 2026",                        "中文 - unifuncs"),
    ("perplexity",     "what is GEO optimization",                "海外 - perplexity"),
    ("firecrawl",      "GeoLook github",                          "海外 - firecrawl"),
    ("exa",            "GeoLook startup",                          "海外 - exa"),
    ("metaso",         "AI search optimization",                   "海外 - metaso"),
    ("search1_search", "GEO 优化工具 github",                      "聚合 - search1_search"),
    ("search1_news",   "GEO AI optimization 2026",                "聚合 - search1_news"),
]

print("=" * 70)
print(" 9 个搜索 provider 冒烟测试")
print("=" * 70)
ok = 0
for prov, q, desc in tests:
    r = S.search(q, prov, count=3, timeout=20)
    if r.get("ok"):
        n = len(r.get("results") or [])
        first = r["results"][0] if r["results"] else {}
        title = (first.get("title") or "(no title)")[:60]
        url = (first.get("url") or "")[:60]
        print(f"  [{prov:14s}] OK  n={n}  time={r.get('response_time',0):.1f}s  first='{title}' @ {url}")
        ok += 1
    else:
        print(f"  [{prov:14s}] FAIL  {r.get('error','')[:160]}")
print(f"\n=== search() 测试：{ok}/{len(tests)} 通过 ===\n")

# 测试 search_then_ask 组合（豆包 302.AI 模式的实际用法）
print("=" * 70)
print(" search_then_ask 组合测试（豆包 302.AI 模式，bocha 搜索 + doubao LLM）")
print("=" * 70)
res = S.ask("doubao", "GeoLook 是什么工具？它跟传统 SEO 比有什么优势？", timeout=60)
print(f"  ok={res.get('ok')}  search_provider={res.get('search_provider')}  skipped={res.get('search_skipped','-')}")
print(f"  search_citations={len(res.get('search_citations') or [])}")
for c in (res.get("search_citations") or [])[:3]:
    print(f"    • {c.get('title','')[:60]}  {c.get('url','')[:60]}")
ans = (res.get("answer") or "").strip()[:300].replace("\n", "\n    ")
print(f"  answer:\n    {ans}")

# 再测一个中文搜索深度问题（用 exa 看论文）
print()
print("=" * 70)
print(" 深度搜索：exa (research paper) + claude-sonnet-5")
print("=" * 70)
sr = S.search("transformer attention mechanism", "exa", count=3, category="research paper")
if sr.get("ok"):
    for r in sr.get("results", []):
        print(f"  • {r.get('title','')[:70]}")
        print(f"    {r.get('url','')[:80]}")
