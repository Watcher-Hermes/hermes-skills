#   Final stable range: 0.60-0.75 depending on MAB confidence
CONFIDENCE_THRESHOLD = 0.70

def decide(query, rules, mab):
    rule_result = rules.match(query)

    if rule_result.confidence > CONFIDENCE_THRESHOLD: