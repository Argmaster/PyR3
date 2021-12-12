########################
 Development Guidelines
########################

There are some rules in how PyR3 should be developed, related to git
branch structure, testing and building. We will make an attempt to
describe them here.

*********************
 Git repo management
*********************

In general this project is making use of a `successfull Git branching
model <https://nvie.com/posts/a-successful-git-branching-model/>`_ With
partial automation with python scripts and some changes.

``main`` and ``develop``
========================

In repo there are two branches that lives next to each other.

The ``develop`` branch contains all in-development code with all
unstable features and changes.

On the other hand ``main`` branch always contains most recent **stable**
code.

Feature branches
================

Feature branches always follows following naming convention with
"feature-" prefix and unique feature name postfix. eg.
"feature-generators", "feature-linux-support"

Also, those branches are always created from ``develop`` branch and they
merge back into ``develop``.

To be sure you wont mess anything in feature branch creation you can use
python script available in this repo in scripts/fork_feature.py:

``python -m scripts.fork_feature <feature-name>``

"feature-" prefix is automatically added so you don't have to include in
script call args.

After you finish working on your feature open a pull request on GitHub
and either wait for request being accepted or if you have necessary
rights, merge it yourself. Don't use scripts/merge_feature.py anymore,
pull requests are better way of managing branch merging in this case.

Release branches (major and minor)
==================================

After adding a bunch of features to ``develop``, make sure you have
described them in ``CHANGELOG.rst`` on ``develop`` branch. Make sure
version tag above feature description matches version tag you are
planning to use for this release.

Release branch have to be drafted from ``develop`` and you should use
``scripts/fork_release.py`` for it unless you are willing to fix all the
messed up version tags. Im sure you don't, so never create release
branch manually via git.

``python -m scripts.fork_release --major``

or

``python -m scripts.fork_release --minor``

Using --patch is highly discouraged, for small changes us hotfix
approach.

After you make sure release branch is **release ready** go to GitHub and
create pull request to merge ``release-x.y.z`` into ``main``. It will
run bunch of tests. **You should wait for tests to succeed.**

Then, If you have enough permissions, you can accept merge.

Merge will cause additional merges to run to sync remote branches, so
after release you have to locally pull changes to both ``main`` and
``develop``. It will also automatically create release with release
notes from ``CHANGELOG.rst`` file.

**PyPI release is not automatically created.**

Hotfix branches (patch)
=======================

Hotfix branches are used to hotfix already existing releases. Therefore
they are forked from release branch patch corresponds to. Make sure you
use ``scripts/fork_hotfix.py`` to create hotfix branch, as all version
tags have to be updated, and for sure you don't want to do it manually.

``python -m scripts.fork_hotfix <version-tag-to-fork-from>``

eg.

``python -m scripts.fork_hotfix v0.3.0``

To merge this branch do the same as with release branch (see **Release
branches (major and minor)**).
