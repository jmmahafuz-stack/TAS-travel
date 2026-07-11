## GitHub Copilot Chat

- Extension: 0.47.0 (prod)
- VS Code: 1.119.0 (8b640eef5a6c6089c029249d48efa5c99adf7d51)
- OS: win32 10.0.26200 x64
- GitHub Account: raufakib418-spec

## Network

User Settings:
```json
  "http.systemCertificatesNode": true,
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 20.205.243.168 (2821 ms)
- DNS ipv6 Lookup: Error (3197 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (2 ms)
- Electron fetch (configured): HTTP 200 (7940 ms)
- Node.js https: timed out after 10 seconds
- Node.js fetch: HTTP 200 (8346 ms)

Connecting to https://api.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.114.22 (1068 ms)
- DNS ipv6 Lookup: Error (680 ms): getaddrinfo ENOTFOUND api.githubcopilot.com
- Proxy URL: None (24 ms)
- Electron fetch (configured): timed out after 10 seconds
- Node.js https: timed out after 10 seconds
- Node.js fetch: HTTP 200 (8682 ms)

Connecting to https://copilot-proxy.githubusercontent.com/_ping:
- DNS ipv4 Lookup: 138.91.182.224 (2068 ms)
- DNS ipv6 Lookup: Error (1676 ms): getaddrinfo ENOTFOUND copilot-proxy.githubusercontent.com
- Proxy URL: None (26 ms)
- Electron fetch (configured): timed out after 10 seconds
- Node.js https: HTTP 200 (6571 ms)
- Node.js fetch: HTTP 200 (8966 ms)

Connecting to https://mobile.events.data.microsoft.com: HTTP 404 (8961 ms)
Connecting to https://dc.services.visualstudio.com: timed out after 10 seconds
Connecting to https://copilot-telemetry.githubusercontent.com/_ping: HTTP 200 (2217 ms)
Connecting to https://telemetry.individual.githubcopilot.com/_ping: HTTP 200 (5824 ms)
Connecting to https://default.exp-tas.com: HTTP 400 (3024 ms)

Number of system certificates: 388

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).