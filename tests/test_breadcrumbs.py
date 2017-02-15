import unittest
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from paka.breadcrumbs import Bread, Crumb


class BreadcrumbsTest(unittest.TestCase):

    def setUp(self):
        self.site_name = "Some site Name"

    def test_breadcrumbs_can_be_converted_to_list(self):
        crumbs = list(Bread(self.site_name))
        self.assertGreater(len(crumbs), 0)

    def test_breadcrumbs_can_be_indexed(self):
        self.assertIsInstance(Bread(self.site_name)[0], Crumb)

    def test_default_site_crumb(self):
        crumb, = Bread(self.site_name)
        self.assertEqual(crumb.label, self.site_name)
        self.assertEqual(crumb.heading, self.site_name)
        self.assertEqual(crumb.url_path, "/")
        self.assertEqual(crumb.extra, {})

    def test_changed_site_url_path(self):
        url_path = "/some/other/"
        crumb, = Bread(self.site_name, url_path=url_path)
        self.assertEqual(crumb.url_path, url_path)

    def test_changed_site_heading(self):
        heading = "something different"
        crumb, = Bread(self.site_name, heading=heading)
        self.assertEqual(crumb.label, self.site_name)
        self.assertEqual(crumb.heading, heading)

    def test_changed_site_extra(self):
        extra = {"a": 1, "b": 2}
        crumb, = Bread(self.site_name, extra=extra)
        self.assertEqual(crumb.extra, extra)

    def test_adding_is_done_in_correct_order(self):
        bcrumbs = Bread(self.site_name)
        label, heading, url_path, extra = "Label", "Heading", "/test/", {1: 2}
        bcrumbs.add(label, heading=heading, url_path=url_path, extra=extra)
        site_crumb, test_crumb = bcrumbs

        self.assertEqual(site_crumb.label, self.site_name)
        self.assertEqual(site_crumb.heading, self.site_name)
        self.assertEqual(site_crumb.url_path, "/")
        self.assertEqual(site_crumb.extra, {})

        self.assertEqual(test_crumb.label, label)
        self.assertEqual(test_crumb.heading, heading)
        self.assertEqual(test_crumb.url_path, url_path)
        self.assertEqual(test_crumb.extra, extra)

    def test_adding_defaults(self):
        label = "some label"
        bcrumbs = Bread(self.site_name)
        bcrumbs.add(label)
        test_crumb = bcrumbs[1]
        self.assertEqual(test_crumb.label, label)
        self.assertEqual(test_crumb.heading, label)
        self.assertIsNone(test_crumb.url_path)
        self.assertEqual(test_crumb.extra, {})

    def test_adding_crumb(self):
        expected_crumb = Crumb(
            "Crumb here", heading="H", url_path="url", extra={1: 2})
        bcrumbs = Bread(self.site_name)
        bcrumbs.add_crumb(expected_crumb)
        site_crumb, test_crumb = bcrumbs
        self.assertEqual(expected_crumb, test_crumb)

    def test_from_crumb(self):
        expected_crumb = Crumb(
            "Crumb here", heading="H", url_path="url", extra={1: 2})
        bcrumbs = Bread.from_crumb(expected_crumb)
        crumb, = bcrumbs
        self.assertEqual(expected_crumb, crumb)

    def test_from_crumbs(self):
        crumbs = (
            Crumb(self.site_name, extra={1: "one"}, url_path="/"),
            Crumb("Second", url_path="/second/"),
            Crumb("Third"))
        bcrumbs = Bread.from_crumbs(crumbs)
        for expected, actual in zip_longest(crumbs, bcrumbs):
            self.assertEqual(expected, actual)

    def test_from_empty_crumbs(self):
        with self.assertRaises(ValueError):
            Bread.from_crumbs(())


class CrumbTest(unittest.TestCase):

    def test_empty_url_path_results_in_none(self):
        crumb = Crumb("label", url_path="")
        self.assertIsNone(crumb.url_path)

    def test_equality_defaults(self):
        args, kwargs = ("a", ), {}
        crumb_a = Crumb(*args, **kwargs)
        crumb_b = Crumb(*args, **kwargs)
        self.assertEqual(crumb_a, crumb_b)

    def test_equality_same_kwargs(self):
        kwargs = {
            "label": "Some label", "url_path": "/url/path",
            "heading": "Same", "extra": {0: 1}}
        crumb_a = Crumb(**kwargs)
        crumb_b = Crumb(**kwargs)
        self.assertEqual(crumb_a, crumb_b)

    def test_equality_different_label(self):
        same_kwargs = {
            "url_path": "/url/path", "heading": "Same", "extra": {1: 2}}
        crumb_a = Crumb(label="a", **same_kwargs)
        crumb_b = Crumb(label="b", **same_kwargs)
        self.assertNotEqual(crumb_a, crumb_b)

    def test_equality_different_url_path(self):
        same_kwargs = {
            "label": "Same", "heading": "Same too", "extra": {3: 4}}
        crumb_a = Crumb(url_path="a", **same_kwargs)
        crumb_b = Crumb(url_path="b", **same_kwargs)
        self.assertNotEqual(crumb_a, crumb_b)

    def test_equality_different_heading(self):
        same_kwargs = {
            "url_path": "/url/path", "label": "Same", "extra": {5: 6}}
        crumb_a = Crumb(heading="a", **same_kwargs)
        crumb_b = Crumb(heading="b", **same_kwargs)
        self.assertNotEqual(crumb_a, crumb_b)

    def test_equality_different_extra(self):
        same_kwargs = {
            "url_path": "/url/path", "heading": "Same", "label": "Same too"}
        crumb_a = Crumb(extra={"a": 1}, **same_kwargs)
        crumb_b = Crumb(extra={"b": 2}, **same_kwargs)
        self.assertNotEqual(crumb_a, crumb_b)
