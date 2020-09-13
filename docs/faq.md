# Frequently Asked Questions and Common Problems

## ValueError: Invalid JSON data returned from network

Occasionally, PurpleAir's API will return invalid JSON. Usually, this means a double quote char or some other delimiter is missing. There is nothing we can do, so this library raise a ValueError.

The only fix is to try again or invalidate or delete the cache that `requests_cache` creates. If the invalid response is cached (it shouldn’t be), you can delete the cache by removing the `cache.sqlite` file it creates in the project’s root directory.

## Unable to open cache or purge cache database, requests will not be cached

This error means there is a problem connecting to the `cache.sqlite` file created by `requests_cache`. The program will still run, but results of API calls will not be cached, so affected programs may hit rate limits.

## No sensor data returned from PurpleAir

This error happens if the API fails to return data with a `results` key, where `results` is mapped to a JSON blob of sensors.

### Rate Limit Error

If this error includes a rate limit message, try again when the rate limit is expired.

### Other Message

If the error message is not a rate limit error, please open a new [issue](https://github.com/ReagentX/purple_air_api/issues) with the full traceback and message.

## Other Crashes and Errors

If your problem is not listed here, please open a new [issue](https://github.com/ReagentX/purple_air_api/issues).
