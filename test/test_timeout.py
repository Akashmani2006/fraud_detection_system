import time

from app.tools.timeout_tools import run_with_timeout


def slow_function():
    print("Slow function started...")
    time.sleep(5)
    return "Finished"


try:
    result = run_with_timeout(
        slow_function,
        2
    )

    print("Result:", result)

except TimeoutError as e:
    print("TIMEOUT TEST PASSED")
    print(e)