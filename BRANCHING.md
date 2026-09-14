# Git Branching Strategy

This project uses a lightweight Git flow based on `main`, `develop`, and
short-lived `feature/*` branches.

`main` represents the deployable state of the project.

`develop` is the integration branch where completed features are combined
before the next release.

Each assignment part is developed on a separate feature branch created from
`develop`. After the work is tested, the feature branch is merged into
`develop` through a pull request.

No direct commits are made to `main` or `develop`.

For this project I am using this approach because the assignment explicitly
requires incremental development and visible Git history. For a team of five
shipping daily, I would recommend a simplified version of this model with
short-lived feature branches and pull requests, although I would avoid
unnecessarily long-lived branches.