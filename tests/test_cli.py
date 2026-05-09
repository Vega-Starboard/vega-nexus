from vega_nexus.cli import classify_task

def test_security_classification():
    assert classify_task('review auth token handling')['risk'] >= 2
