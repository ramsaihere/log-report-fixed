There is an Apache-style access log at /app/access.log. Analyze the traffic and write a
summary report as JSON to /app/report.json.

The report must be a single JSON object with exactly these three keys:

1. "total_requests": an integer, the total number of log lines (requests) in the file.
2. "unique_ips": an integer, the number of distinct client IP addresses that made requests.
3. "top_path": a string, the request path (e.g. "/index.html") that was requested more
   often than any other path in the log.

Write the finished JSON object to /app/report.json before you finish.
