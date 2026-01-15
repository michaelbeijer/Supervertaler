"""modules.superdocs (deprecated)

The in-app Superdocs generator and viewer were removed in favor of the online GitBook
documentation:

    https://supervertaler.gitbook.io/superdocs/

This module remains as a tiny shim to prevent accidental imports in older code paths.
"""


def __getattr__(name: str):
    raise ImportError(
        "The 'modules.superdocs' module has been removed. Use the online Superdocs at "
        "https://supervertaler.gitbook.io/superdocs/"
    )


__all__: list[str] = []
