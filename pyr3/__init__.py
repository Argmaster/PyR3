# -*- coding: utf-8 -*-

__major__ = 0
__minor__ = 0
__patch__ = 1
__suffix__ = None

__version__ = f"v{__major__}.{__minor__}.{__patch__}" + (
    "" if not __suffix__ else f"-{__suffix__}"
)
__version_no_suffix__ = f"v{__major__}.{__minor__}.{__patch__}"
