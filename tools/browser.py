import asyncio
from playwright.async_api import async_playwright

# User agent to avoid bot detection
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


async def _browse(url: str, action: str = "text", selector: str = None):
    """Internal browser helper."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=USER_AGENT)
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        result = {}

        if action == "text":
            result["content"] = await page.inner_text("body")

        elif action == "html":
            result["content"] = await page.content()

        elif action == "screenshot":
            path = selector or "screenshot.png"
            await page.screenshot(path=path, full_page=True)
            result["saved_to"] = path

        elif action == "links":
            links = await page.eval_on_selector_all(
                "a[href]",
                "elements => elements.map(e => ({text: e.innerText.trim(), href: e.href}))"
            )
            result["links"] = links[:50]

        elif action == "click" and selector:
            await page.click(selector)
            await page.wait_for_timeout(2000)
            result["content"] = await page.inner_text("body")

        elif action == "type" and selector:
            parts = selector.split("|", 1)
            if len(parts) == 2:
                await page.fill(parts[0], parts[1])
                result["typed"] = True

        result["title"] = await page.title()
        result["url"] = page.url

        await browser.close()
        return result


def browse(url: str, action: str = "text", selector: str = None):
    """
    Browse a URL and extract content.

    Actions:
        - text: Get page text content
        - html: Get full HTML
        - screenshot: Save screenshot
        - links: Extract all links
        - click: Click a selector
        - type: Type into a field (selector = "css_selector|text_to_type")
    """
    try:
        result = asyncio.run(_browse(url, action, selector))
        return {"success": True, **result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search(query: str):
    """
    Search the web using DuckDuckGo.
    Uses the duckduckgo_search library for reliable results.
    Falls back to Playwright scraping if library is not available.
    """
    # Try using duckduckgo-search library first (most reliable)
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=10):
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", ""),
                })

        return {"success": True, "query": query, "results": results}

    except ImportError:
        # Fallback to playwright scraping
        pass
    except Exception as e:
        # If DDGS fails, try playwright
        pass

    # Fallback: Playwright-based search
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    try:
        result = asyncio.run(_search(url))
        return {"success": True, **result}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def _search(url: str):
    """Internal search helper using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=USER_AGENT)
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for results to load
        await page.wait_for_timeout(2000)

        # Try multiple selector patterns (DuckDuckGo changes these)
        results = await page.evaluate("""
            () => {
                const results = [];

                // Pattern 1: DuckDuckGo HTML lite
                const items = document.querySelectorAll('.result, .web-result, .results_links');
                for (const item of items) {
                    const titleEl = item.querySelector('.result__title, .result__a, a.result__url, h2 a, a');
                    const snippetEl = item.querySelector('.result__snippet, .result__body, .snippet');
                    const urlEl = item.querySelector('.result__url, .result__extras__url, a');

                    if (titleEl) {
                        results.push({
                            title: titleEl.innerText ? titleEl.innerText.trim() : '',
                            snippet: snippetEl ? snippetEl.innerText.trim() : '',
                            url: urlEl ? (urlEl.href || urlEl.innerText.trim()) : ''
                        });
                    }
                }

                // Pattern 2: If no results found, try generic link extraction
                if (results.length === 0) {
                    const links = document.querySelectorAll('a[href*="http"]');
                    for (const link of links) {
                        const href = link.href;
                        if (href && !href.includes('duckduckgo.com') && link.innerText.trim().length > 5) {
                            results.push({
                                title: link.innerText.trim(),
                                snippet: '',
                                url: href
                            });
                        }
                    }
                }

                return results.slice(0, 10);
            }
        """)

        await browser.close()
        return {"query": url.split("q=")[1].replace("+", " "), "results": results}
