# Disposable Workflow Privilege Check hosted tests

Test-only repository for v0.1.1. Not a production release. No real secrets or cloud credentials are used. The scanner runs from a fixed commit; PR content is read from Git objects without checkout. Fixture workflows are manual-only, except an inert workflow_run filter in the grant case.

Cases: neutral inherited edit, known grants, and unknown inherited/explicit transition, each from a branch and a fork where GitHub permits it. Incomplete scanner exits are expected failures of the scan step; the surrounding test passes only when the expected result and summary are observed.

The summary capture hook is test instrumentation; the published scanner code is unchanged.
