SimpleMatch
===========

SimpleMatch is a replacement for regular expressions that lets you write non-developer
readable/writeable matching expressions.

To install::

  $ pip install simex

To use:

.. code-block:: python

  >>> from simex import simex
  >>> LINK_EXPRESSION = """<a href="{{ url }}">{{ anything }}</a>"""
  >>> exp = simex(LINK_EXPRESSION, regexes={"url": r"(.*?)", "anything": r".*?"})
  >>> exp.match("""<a href="http://www.cnn.com">CNN</a>""") is not None
  True

  >>> exp = simex(LINK_EXPRESSION, regexes={"url": r"(.*?)"})
  >>> exp.match("""<a href="http://www.cnn.com">{{ anything }}</a>""") is not None
  True

  >>> exp = simex(LINK_EXPRESSION, regexes={"url": r"(.*?)"})
  >>> exp.search("""Pre text <a href="http://x.com">{{ anything }}</a> post text""") is not None
  True