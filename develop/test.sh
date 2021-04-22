# Unittest and coverage using pytest
function unittest() {
    echo "==============================================="
    echo "Running Unittests with coverage"
    pytest --cov=vzmi.ychaos --cov-report term-missing tests --durations=5
    rm .coverage*
}

unittest