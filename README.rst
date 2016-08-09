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
  >>> exp = simex(LINK_EXPRESSION, url=r"(.*?)", anything=r".*?")
  >>> exp.match("""<a href="http://www.cnn.com">CNN</a>""") is not None
  True

  >>> exp = simex(LINK_EXPRESSION, url=r"(.*?)")
  >>> assert exp.match("""<a href="http://www.cnn.com">{{ anything }}</a>""")
  True

  >>> exp = simex(LINK_EXPRESSION, url=r"(.*?)")
  >>> assert exp.search("""Pre text <a href="http://x.com">{{ anything }}</a> post text""")
  True