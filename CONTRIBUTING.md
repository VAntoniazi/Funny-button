# Contributing

Thanks for improving Funny Button.

## Development

This is a lightweight static project with no build or runtime dependencies. Make focused changes in index.html and keep the interface useful on small and large screens. Do not add libraries unless there is a clear benefit.

## Validate a change

1. Run node --test tests/*.test.mjs (Node.js 22+ recommended).
2. Open index.html locally and check mouse/trackpad behavior.
3. Check touch interaction, keyboard focus, and the affirmative link.
4. Check that the moving button stays visible after viewport changes.
5. Update README or docs when behavior changes.

Small, descriptive commits are preferred, for example: fix: keep evasive button inside viewport.

main is the only permanent branch; if a short-lived branch is needed for collaboration, merge it and delete it afterward.
