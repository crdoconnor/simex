SimEx
=====

SimEx is a tool that lets you write simple, readable equivalents of regular expressions that
compile down to regular expressions.

This is useful for:

* Improving the readability and maintainability of code that uses long regexes with a lot of escaped characters.
* Allowing non-developers to read and understand simple regex-equivalents and potentially even write their own.

Simex is *not* a full replacement for regular expressions and its use is not suitable everywhere a regex is used.

It is ideally used where you usually want to compare two strings but you occasionally need to compare two
strings with a pattern embedded within them.

It is an embodiment of `the rule of least power <https://en.wikipedia.org/wiki/Rule_of_least_power>`_.

To install::

  $ pip install simex


Example
-------

.. code-block:: python

  >>> from simex import Simex
  >>> simex = Simex({"url": r".*?", "anything": r".*?"})
  >>> regex = simex.compile("""<a href="{{ url }}">{{ anything }}</a>""")
  >>> regex.match("""<a href="http://www.cnn.com">CNN</a>""") is not None
  True


Do I have to define all of the sub-regular expressions myself?
--------------------------------------------------------------

No. SimEx also contains a built in library of commonly used regular expressions.

This will also work:

.. code-block:: python

  >>> from simex import Simex
  >>> my_simex = DefaultSimex()
  >>> regex = my_simex.compile("""<a href="{{ url }}">{{ anything }}</a>""")
  >>> regex
  re.compile(r'\<a\ href\=\"(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\\'\/\\\+&amp;%\$#_]*)?\"\>.*?\<\/a\>', re.UNICODE)

  >>> regex.match("""<a href="http://www.cnn.com">CNN</a>""") is not None

All regexes in the existing library can be overridden, and more can be added, e.g.

.. code-block:: python

  >>> simex = DefaultSimex({"url": r".*?", "mycode": r"[A-Z][0-9][0-9][0-9]"})

Currently there are five in the list of pre-defined regexes:

* URL
* Email
* Integer
* Number
* Anything

Pull requests with commonly required non-controversial regexes are welcome.


Using {{ and }} creates conflicts for me! Why not [[[ and ]]]?
--------------------------------------------------------------

{{ and }} have a special meaning in some languages which you may want to use
with simex - e.g. jinja2.

In order to prevent confusion in such circumstances, you can define your
own delimeters:

.. code-block:: python

  >>> from simex import Simex
  >>> simex = Simex(open_delimeter="[[[", close_delimeter="]]]")
  >>> simex.compile("""<a href="[[[ url ">[[[ anything ]]]</a>""")
  >>> simex.match("""<a href="http://www.cnn.com">CNN</a>""") is not None


Matching exact strings
----------------------

By default a simex will not match an exact string. i.e. it will produce:

.. code-block:: python

  >>> from simex import Simex
  >>> simex = Simex({"url": r".*?", "anything": r".*?"})
  >>> regex = simex.compile("""<a href="{{ url }}">{{ anything }}</a>""")
  >>> regex
  re.compile(r'\<a\ href\=\".*?\"\>.*?\<\/a\>', re.UNICODE)
  >>> regex.match("""<a href="http://www.cnn.com">CNN</a> THERE IS MORE TEXT""") is not None
  True

However, if you want, simexes can be used to do exact matching. For example:

.. code-block:: python

  >>> from simex import Simex
  >>> simex = Simex({"url": r".*?", "anything": r".*?"}, exact=True)
  >>> regex = simex.compile("""<a href="{{ url }}">{{ anything }}</a>""")
  >>> regex
  re.compile(r'^\<a\ href\=\".*?\"\>.*?\<\/a\>$', re.UNICODE)
  >>> regex.match("""<a href="http://www.cnn.com">CNN</a>""") is not None
  True
  >>> regex.match("""<a href="http://www.cnn.com">CNN</a> THERE IS MORE TEXT""") is not None
  False

Matching can also treat whitespace (tabs, spaces and newlines) as interchangeable. For example:

.. code-block:: python

  >>> from simex import Simex
  >>> simex = Simex({"url": r".*?", "anything": r".*?"}, flexible_whitespace=True)
  >>> regex = simex.compile("""<a href="{{ url }}">{{ anything }}</a>""")
  >>> regex
  re.compile(r'\<a\\s+href\=\".*?\"\>.*?\<\/a\>', re.UNICODE)
  >>> regex.match("""<a   href="http://www.cnn.com">CNN</a>""") is not None
  True

.. code-block:: python



How does it work?
-----------------

The regular expression simply escapes an entire simexpression, except for the
components surrounded by {{ and }}, which it replaces with defined regular
expressions - like "email" or "anything" or "number" defined in the dict.
