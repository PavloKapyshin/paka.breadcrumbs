import unittest

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


class CrumbTest(unittest.TestCase):

    def test_empty_url_path_results_in_none(self):
        crumb = Crumb("label", url_path="")
        self.assertIsNone(crumb.url_path)
