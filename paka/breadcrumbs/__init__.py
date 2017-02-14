"""Helpers for breadcrumbs navigation building."""

try:
    from collections.abc import Sequence
except ImportError:  # pragma: no cover
    from collections import Sequence


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
        """Create and "add" (append) crumb.

        Note
        ----
        For accepted parameters and their behaviour, see :py:class:`Crumb`
        constructor's documentation.

        """
        self._crumbs.append(Crumb(*args, **kwargs))
