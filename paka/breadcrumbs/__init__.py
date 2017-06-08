"""Helpers for breadcrumbs navigation building."""

from __future__ import unicode_literals

import operator
try:
    from collections.abc import Sequence
except ImportError:  # pragma: no cover
    from collections import Sequence
try:
    from itertools import imap
except ImportError:
    imap = map  # pylint: disable=invalid-name

import markupsafe


def _crumb_to_kwargs(crumb):
    return {
        "label": crumb.label, "heading": crumb.heading,
        "url_path": crumb.url_path, "extra": crumb.extra}


class Crumb(object):  # pylint: disable=too-few-public-methods
    """Item of :py:class:`Bread`."""

    def __init__(self, label, url_path=None, heading=None, extra=None):
        """Create item with label and other fields.

        Parameters
        ----------
        label: str
            Usually some text associated with item.
        url_path: str
            URL path of an item.
        heading: str
            Usually an associated heading (if value of ``heading`` is
            considered ``False``, value of ``label`` is used instead).
            This can be used, for example, to make page headings on website
            breadcrumbs-dependent.
        extra: dict
            Dictionary that may carry "extra" information you want to
            associate with a crumb.

        """
        self.label = label
        self.url_path = url_path or None
        self.heading = heading or label
        self.extra = extra or {}

    def __eq__(self, other):
        """Check fields of other are equal to fields of self."""
        return _crumb_to_kwargs(self) == _crumb_to_kwargs(other)


_get_crumb_label = operator.attrgetter("label")  # pylint: disable=invalid-name


class Bread(Sequence):
    r"""Sequence of :py:class:`Crumb`\ s."""

    def __init__(self, label, url_path="/", heading=None, extra=None):
        """Create sequence with one initial crumb.

        Initial crumb is also called "site crumb", because it usually
        has site name in ``label``, and ``/`` in ``url_path``.

        Parameters
        ----------
        label: str
            Label of initial crumb.
        url_path: str
            URL path of initial crumb. By default, ``/``.
        heading: str
            Heading of initial crumb. As in :py:class:`Crumb`, ``label``
            is used if ``heading`` is "not provided".
        extra: dict
            Additional information for initial crumb.

        Note
        ----
        For purpose of parameters, see :py:class:`Crumb` constructor's
        documentation.

        """
        site_crumb = Crumb(
            label, url_path=url_path, heading=heading, extra=extra)
        self._crumbs = [site_crumb]

    def __getitem__(self, index):
        """Get :py:class:`Crumb` by index."""
        return self._crumbs[index]

    def __len__(self):
        """Return total number of crumbs."""
        return len(self._crumbs)

    def add(self, *args, **kwargs):
        """Create and append crumb.

        Note
        ----
        For accepted parameters and their behaviour, see :py:class:`Crumb`
        constructor's documentation.

        """
        self._crumbs.append(Crumb(*args, **kwargs))

    def add_crumb(self, crumb):
        """Append instance of :py:class:`Crumb`."""
        self._crumbs.append(crumb)

    def get_title(self, separator):
        """Return crumb labels joined by separator & spaces in reverse order.

        Parameters
        ----------
        separator: str or markupsafe.Markup
            String to put between labels.

        Returns
        -------
        markupsafe.Markup
            Escaped string suitable for putting into HTML ``title``.

        """
        escape = markupsafe.escape
        labels = imap(escape, imap(_get_crumb_label, reversed(self._crumbs)))
        return markupsafe.Markup(
            " {} ".format(escape(separator)).join(labels))

    @classmethod
    def from_crumb(cls, crumb):
        """Create sequence with one (initial) crumb.

        Parameters
        ----------
        crumb: Crumb
            Initial crumb.

        """
        return cls(**_crumb_to_kwargs(crumb))

    @classmethod
    def from_crumbs(cls, crumbs):
        r"""Create sequence from sequence of :py:class:`Crumb`\ s."""
        crumbs = tuple(crumbs)
        if not crumbs:
            raise ValueError("crumbs must have at least one item")
        bcrumbs = cls.from_crumb(crumbs[0])
        for crumb in crumbs[1:]:
            bcrumbs.add_crumb(crumb)
        return bcrumbs
