# AGENTS.md

## Cursor Cloud specific instructions

### What this repository is
This is a **documentation-only repository** for the **VAD (Verifiable AI Development)** methodology. It contains prose/specification content only:

- `README.md` — English methodology document.
- `README.ko.md` — Korean translation.

There is **no application source code, no package manifest/lockfile, no build system, no automated tests, and no runnable services**. The `README.md` references `rfcs/0001-vad-core.md` and `CONTRIBUTING.md`, but those files do not exist yet.

### Environment / dependencies
- Nothing to install. There is no lockfile or manifest, so the startup update script is intentionally a no-op.
- Node and Python are available on the VM if you need ad-hoc tooling (e.g. a Markdown previewer), but none is required or configured by the repo.

### "Build / run / test"
- **Build:** nothing to build (plain Markdown).
- **Run:** nothing to run. To preview the docs, render Markdown with any renderer, e.g. serve the repo statically and view the file, or convert to HTML with a Markdown tool.
- **Test / lint:** no test or lint config exists. At most you could run an external Markdown linter/link-checker, but none is committed.

### Working in this repo
- Treat changes as documentation edits. Verify by rendering the Markdown and checking it displays and links resolve.
- Keep edits minimal and consistent between `README.md` and `README.ko.md` when content is mirrored.
