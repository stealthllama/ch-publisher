# clickhelper
This GitHub Action runs a scheduled job that performs various actions on publications that are hosted on a ClickHelp documentation portal.

### Configuration
The `publications.yaml` file contains details of the publications that will be published.

For example:
```yaml
dragos-platform-release-notes:
  project: release-notes
  title: Release Notes
  update: Partial
  visibility: Restricted
  output_tags:
    - OnlineDoc
    - Platform_3.0
    - Platform_3.0.1
    - Platform_3.0.2
```
