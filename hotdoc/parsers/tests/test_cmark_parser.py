# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: disable=invalid-name

import unittest
from hotdoc.parsers import cmark
from hotdoc.core.doc_database import DocDatabase
from hotdoc.core.links import LinkResolver, Link


class TestParser(unittest.TestCase):
    def setUp(self):
        self.doc_database = DocDatabase()
        self.link_resolver = LinkResolver(self.doc_database)
        self.link_resolver.add_link(Link("here.com", "foo", "foo"))

    def assertOutputs(self, inp, expected):
        ast = cmark.gtkdoc_to_ast(inp, self.link_resolver)
        out = cmark.ast_to_html(ast, self.link_resolver)
        self.assertEqual(out, expected)

    def test_basic(self):
        inp = u'a'
        self.assertOutputs(inp, u"<p>a</p>\n")

    def test_unicode(self):
        inp = u'”'
        self.assertOutputs(inp, u"<p>”</p>\n")

    def test_input_none(self):
        inp = None
        with self.assertRaises(TypeError):
            ast = cmark.gtkdoc_to_ast(inp, self.link_resolver)
            self.assertEqual(ast, None)

    def test_resolver_none(self):
        inp = u'a'
        self.link_resolver = None
        self.assertOutputs(inp, u"<p>a</p>\n")


class TestGtkDocExtension(unittest.TestCase):
    def setUp(self):
        self.doc_database = DocDatabase()
        self.link_resolver = LinkResolver(self.doc_database)
        self.link_resolver.add_link(Link("here.com", "foo", "foo"))

    def assertOutputs(self, inp, expected):
        ast = cmark.gtkdoc_to_ast(inp, self.link_resolver)
        out = cmark.ast_to_html(ast, self.link_resolver)
        self.assertEqual(out, expected)
        return ast

    def test_existing_link(self):
        inp = u"this : #foo is a link !"
        self.assertOutputs(
            inp, '<p>this : <a href="here.com">foo</a> is a link !</p>\n')

    def test_missing_link(self):
        inp = u"this : #fo is not a link .."
        self.assertOutputs(
            inp, u'<p>this : <a href="fo"></a> is not a link ..</p>\n')

    def test_modified_link(self):
        inp = u"this : #foo is a link !"
        ast = self.assertOutputs(
            inp, '<p>this : <a href="here.com">foo</a> is a link !</p>\n')
        self.link_resolver.upsert_link(
            Link("there.com", "ze_foo", "foo"),
            overwrite_ref=True)
        out = cmark.ast_to_html(ast, self.link_resolver)
        self.assertEqual(
            out,
            u'<p>this : <a href="there.com">ze_foo</a> is a link !</p>\n')

    def test_syntax_boundaries(self):
        # Make sure we don't parse type links inside words
        inp = u"this : yo#foo is a link !"
        self.assertOutputs(
            inp,
            u'<p>this : yo#foo is a link !</p>\n')

        # Make sure the function link syntax doesn't take precedence
        # over classic links.
        inp = u"this is [a link]() however"
        self.assertOutputs(
            inp,
            u'<p>this is <a href="">a link</a> however</p>\n')

        # Make sure we respect code blocks
        inp = u"And `this a code block`()"
        self.assertOutputs(
            inp,
            u'<p>And <code>this a code block</code>()</p>\n')

        inp = u"And `this #too`"
        self.assertOutputs(
            inp,
            u'<p>And <code>this #too</code></p>\n')

        # Boundaries should be acceptable here
        inp = u"function_link()"
        self.assertOutputs(
            inp,
            u'<p><a href="function_link"></a></p>\n')
