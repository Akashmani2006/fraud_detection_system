from concurrent.futures import ThreadPoolExecutor, TimeoutError


def run_with_timeout(function, timeout_seconds, *args, **kwargs):

    with ThreadPoolExecutor(max_workers=1) as executor:

        future = executor.submit(
            function,
            *args,
            **kwargs
        )

        try:
            return future.result(timeout=timeout_seconds)

        except TimeoutError:
            raise TimeoutError(
                f"Agent timed out after {timeout_seconds} seconds"
            )