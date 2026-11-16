"""Your tests. Each milestone in README.md gets one here: write the test first, then make it pass.

They start skipped. Remove the `skip` line as you work on each milestone.
"""
import pytest
import re
from app.core import milestone_1, clean_text, RAW_CORPUS
from app.storage import Store


# Milestone 1: Collect a small corpus of product descriptions for a specific category.
def test_milestone_1(tmp_path):
    store_file = str(tmp_path / "test_store.json")
    result = milestone_1(category="Handcrafted Leather Goods", data_path=store_file)

    # 1. Corpus validation
    assert result["category"] == "Handcrafted Leather Goods"
    assert result["count"] == 20
    assert result["total_words"] > 500
    assert len(result["corpus"]) == 20

    # 2. Text cleaning checks on every item
    for item in result["corpus"]:
        assert item["name"]
        assert item["category"] == "Handcrafted Leather Goods"
        desc = item["cleaned_description"]
        assert len(desc) > 30, f"Description too short: {desc}"

        # No HTML tags
        assert not re.search(r'<[^>]+>', desc), f"Found HTML tags in: {desc}"
        # No unescaped or raw HTML entities
        assert "&amp;" not in desc
        assert "&quot;" not in desc
        assert "&nbsp;" not in desc
        assert "&bull;" not in desc
        # No boilerplate tags
        assert not re.search(r'(?i)\bSKU\s*:', desc), f"Found SKU in: {desc}"
        assert not re.search(r'(?i)\bPrice\s*:', desc), f"Found Price in: {desc}"

    # 3. Persistence validation
    store = Store(store_file)
    assert store.get("category") == "Handcrafted Leather Goods"
    assert store.get("total_products") == 20
    assert len(store.get("corpus")) == 20


def test_clean_text_removes_html_entities_and_boilerplate():
    raw_sample = (
        "<p>Handcrafted with <strong>100% full-grain leather</strong> &amp; solid brass rivets.&nbsp;</p>"
        "<div>SKU: TEST-999 | Price: $120.00 USD</div>"
        "<p>Free shipping on orders over $50. 30-day money-back guarantee.</p>"
    )
    cleaned = clean_text(raw_sample)

    assert "<p>" not in cleaned
    assert "<strong>" not in cleaned
    assert "&amp;" not in cleaned
    assert "&nbsp;" not in cleaned
    assert "TEST-999" not in cleaned
    assert "$120.00" not in cleaned
    assert "Free shipping" not in cleaned
    assert "30-day" not in cleaned
    assert "Handcrafted with 100% full-grain leather & solid brass rivets." in cleaned


def test_cli_collect(capsys, monkeypatch, tmp_path):
    from app.cli import main
    monkeypatch.setenv("DATA_PATH", str(tmp_path / "cli_store.json"))
    main(["collect"])
    captured = capsys.readouterr().out
    assert "Milestone 1: Data Collection & Text Cleaning" in captured
    assert "Handcrafted Leather Goods" in captured
    assert "Total Products Collected: 20" in captured



# Milestone 2: Implement the byte-pair tokenizer and generate embeddings for product text.
@pytest.mark.skip(reason="remove this line when you start milestone 2")
def test_milestone_2():
    raise NotImplementedError("write the test for milestone 2")


# Milestone 3: Build the causal self-attention mechanism and assemble the transformer block.
@pytest.mark.skip(reason="remove this line when you start milestone 3")
def test_milestone_3():
    raise NotImplementedError("write the test for milestone 3")


# Milestone 4: Train the GPT model using the collected product descriptions.
@pytest.mark.skip(reason="remove this line when you start milestone 4")
def test_milestone_4():
    raise NotImplementedError("write the test for milestone 4")


# Milestone 5: Implement a text generation feature that creates new product descriptions from a prompt.
@pytest.mark.skip(reason="remove this line when you start milestone 5")
def test_milestone_5():
    raise NotImplementedError("write the test for milestone 5")


# Milestone 6: Develop a CLI for users to input product details and receive generated descriptions.
@pytest.mark.skip(reason="remove this line when you start milestone 6")
def test_milestone_6():
    raise NotImplementedError("write the test for milestone 6")
