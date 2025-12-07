# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import re
from functools import total_ordering

from packaging.version import parse


@total_ordering
class LooseVersion(object):
    """
    Lightweight compatibility wrapper to replace distutils.version.LooseVersion.

    It delegates comparison/ordering to packaging.version.parse while exposing
    ``version`` and ``vstring`` attributes that the existing code expects.
    """

    __slots__ = ("_inner",)

    def __init__(self, version):
        if isinstance(version, LooseVersion):
            self._inner = version._inner  # pylint: disable=protected-access
        else:
            self._inner = parse(str(version))

    def __repr__(self):
        return "LooseVersion({})".format(str(self._inner))

    def __str__(self):
        return str(self._inner)

    def __hash__(self):
        return hash(self._inner)

    def _coerce_other(self, other):
        if isinstance(other, LooseVersion):
            return other._inner  # pylint: disable=protected-access
        return parse(str(other))

    def __eq__(self, other):
        return self._inner == self._coerce_other(other)

    def __lt__(self, other):
        return self._inner < self._coerce_other(other)

    @property
    def vstring(self):
        return str(self._inner)

    @property
    def version(self):
        release = getattr(self._inner, "release", None)
        if release:
            return release

        # Fallback for legacy version objects without a release tuple
        parts = re.split(r"\D+", str(self._inner))
        return tuple(int(p) for p in parts if p)
