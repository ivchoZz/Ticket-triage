from classifier import parse_response

def test_valid_response():
    raw = '{"category": "billing", "urgency": "high", "summary": "Double charge."}'
    result = parse_response(raw)
    assert result["category"] == "billing"
    assert result["urgency"] == "high"

def test_text_instead_of_json_returns_none():
    assert parse_response("Sure! Here is the JSON you asked for.") is None


def test_refusal_returns_none():
    raw = '{"error": "I cannot comply with that."}'
    assert parse_response(raw) is None


def test_unknown_category_returns_none():
    raw = '{"category": "pizza", "urgency": "low", "summary": "x"}'
    assert parse_response(raw) is None


def test_unknown_urgency_returns_none():
    raw = '{"category": "billing", "urgency": "extreme", "summary": "x"}'
    assert parse_response(raw) is None


def test_json_that_is_not_a_dict_returns_none():
    assert parse_response("[1, 2, 3]") is None