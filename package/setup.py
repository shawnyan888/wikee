#!/usr/bin/env python
#

import distutils.core

version = "0.1"

distutils.core.setup(
    name="groot",
    version=version,
    packages=["groot"],
    author="Shawn Yan",
    author_email="shawn.yan@latticesemi.com",
    url="https://github.com/unknown/none",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="General Modules. ",
    long_description=open("README").read()
    )