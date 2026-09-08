from app.search.wikipedia import WikipediaSearchEngine


def test_wikipedia_search():
    engine = WikipediaSearchEngine()

    results = engine.search("machine learning")

    assert isinstance(results, list)

    if results:
        assert "title" in results[0]
        assert "snippet" in results[0]
