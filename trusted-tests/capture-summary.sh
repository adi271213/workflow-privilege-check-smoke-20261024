# Test-only hook: preserve the real composite step's summary before runner cleanup.
# The outer Actions bash retains this trap; the inner bootstrap replaces its own
# trap to clean up its venv. The scanner source is unmodified.
wpc_capture_summary() {
  wpc_exit_status=$?
  if [[ -n "${GITHUB_STEP_SUMMARY:-}" && -f "$GITHUB_STEP_SUMMARY" ]]; then
    cp -- "$GITHUB_STEP_SUMMARY" "$RUNNER_TEMP/wpc-summary.md" || true
  fi
  return "$wpc_exit_status"
}
trap wpc_capture_summary EXIT
