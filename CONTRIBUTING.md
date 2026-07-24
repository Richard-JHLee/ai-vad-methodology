# Contributing to VAD

Thank you for helping improve **Verifiable AI Development (VAD)**.

VAD is an early draft methodology. Contributions that add practical evidence,
counterexamples, clearer wording, or better templates are especially welcome.

## Ways to contribute

* Improve documentation under `docs/`
* Propose or revise RFCs under `rfcs/`
* Refine templates under `templates/`
* Add language- or stack-specific examples under `examples/`
* Share real project experience using the format in [README.md](./README.md)
* Open issues for open questions, failures, or process overhead concerns

## Ground rules

1. Keep changes reviewable. Prefer small pull requests.
2. Distinguish **proposal** from **proven practice**.
3. Do not claim VAD guarantees safe AI-generated code.
4. Prefer examples grounded in real systems over abstract slogans.
5. Follow the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Pull request checklist

* [ ] Linked to an issue or RFC when relevant
* [ ] Explains why the change helps verifiable AI-assisted development
* [ ] Updates English docs; Korean (`README.ko.md` or mirrored docs) when practical
* [ ] Does not introduce unrelated refactoring of the whole repository

## RFC process (draft)

1. Discuss the idea in an issue when possible.
2. Copy the structure of [`rfcs/0001-vad-core.md`](./rfcs/0001-vad-core.md).
3. Add `rfcs/NNNN-short-title.md` and update [`rfcs/README.md`](./rfcs/README.md).
4. Mark status as `Draft` until maintainers accept it.

## Local preview

This repository is documentation-first. No build step is required. Edit Markdown
and open a pull request against `main`.

## License

By contributing, you agree that your contributions are licensed under
[CC-BY-4.0](./LICENSE), matching the rest of this repository’s methodology
materials.
