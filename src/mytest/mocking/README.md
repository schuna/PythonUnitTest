# Understanding the Python Mock Object Library 요점 정리

[https://realpython.com/python-mock-library/](https://realpython.com/python-mock-library/)

## 목표

1. Create Python mock objects using Mock
2. Assert you’re using objects as you intended
3. Inspect usage data stored on your Python mocks
4. Configure certain aspects of your Python mock objects
5. Substitute your mocks for real objects using patch()
6. Avoid common problems inherent in Python mocking

## Mocking이란?

1. A mock object substitutes and imitates a real object within a <span style="color:#00FF00">testing environment</span>.
2. One reason to use Python mock objects is to <span style="color:#00FF00">control your code’s behavior</span> during
   testing
3. For example, if your code makes HTTP requests to external services, <br>then your tests execute predictably only so
   far as the services are behaving as you expected. <br>Sometimes, a temporary change in the behavior of these external
   services can cause <br><span style="color:#FFA500">intermittent failures</span> within your test suite.
4. Because of this, it would be better for you to test your code in a <span style="color:#00FF00">controlled
   environment</span>. <br>Replacing the actual request with a mock object would allow you to <br>simulate external
   service outages and successful responses in a predictable way.

## The Python Mock Library

### The Mock Object

1. Begin by instantiating a new Mock instance

```python
from unittest.mock import Mock

mock = Mock()
print(mock)
# <Mock id='1945673309896'>
```

2. substitute an object in your code with your new Mock

```python
# Pass mocking as an argument to do_something()
from unittest.mock import Mock

mock = Mock()


def do_something(arg):
    pass


do_something(mock)

# patch the json library
json = mock
```

3. When you substitute an object in your code, <span style="color:#00FF00">the Mock must look like the real
   object</span> it is replacing. <br>Otherwise, your code <span style="color:#FFA500">will not be able to use the
   Mock</span> in place of the original object.
4. For example, if you are mocking the json library and your program calls dumps(), <br>then your Python mock object
   <span style="color:#FFA500">must also contain dumps()</span>.

### Lazy Attributes and Methods

1. A Mock must simulate any object that it replaces. <br> To achieve such flexibility, <span style="color:#00FF00">it
   creates its attributes when you access them</span>
2. Since Mock can create arbitrary attributes <span style="color:#00FF00">on the fly</span>, it is suitable to replace
   any object
3. If you’re mocking the json library, and you call dumps(), <br>the Python mock object will create the method so
   that <span style="color:#00FF00">its interface can match the library’s interface</span>

```python
from unittest.mock import Mock

json = Mock()
json.dumps()
# <Mock name='mocking.dumps()' id='3001570410632'>
```

4. Notice two key characteristics of this mocked version of dumps()
    1. Unlike the real dumps(), this mocked method requires no arguments. <br>In fact, it
       will <span style="color:#00FF00">accept any arguments</span> that you pass to it.
    2. The return value of dumps() is also a Mock. <br>The capability of Mock to recursively define other mocks allows
       for you to use mocks in complex situations

```python
from unittest.mock import Mock

json = Mock()
json.loads('{"k": "v"}').get('k')
# <Mock name='mocking.loads().get()' id='3001574553032'>
```

    3. Because the return value of each mocked method is also a Mock, you can use your mocks in a multitude of ways.

### Assertions and Inspection

1. Mock instances store data on how you used them
2. For instance, you can see if you called a method, how you called the method, and so on
    1. First, you can assert that your program used an object as you expected
    2. Second, you can view special attributes to understand how your application used an object

```python
from unittest.mock import Mock

json = Mock()
json.loads('{"k": "v"}').get('k')
# <Mock name='mocking.loads().get()' id='3001574553032'>

# assertions to test whether you called loads() as you expected
json.loads.assert_called()
json.loads.assert_called_once()
json.loads.assert_called_with('{"k": "v"}')
json.loads.assert_called_once_with('{"k": "v"}')

# If an assertion fails, the mocking will raise an AssertionError
json.loads.assert_called_once_with('{"k": "v"}')
'''
Traceback (most recent call last):
  File "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\lib\code.py", line 90, in runcode
    exec(code, self.locals)
  File "<input>", line 1, in <module>
  File "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\lib\unittest\mock.py", line 888, in assert_called_once_with
    raise AssertionError(msg)
AssertionError: Expected 'loads' to be called once. Called 2 times.
'''

# Number of times you called loads():
json.loads.call_count
# 1

# The las loads() call
json.loads.call_args
# call('{"k": "v"}')

# List of loads() calls:
json.loads.call_args_list
# [call('{"k": "v"}')]

# List of calls to json's methods (recursively):
json.method_calls
# [call.loads('{"k": "v"}')]
```

### Managing a Mock’s Return Value

One reason to use mocks is to control your code’s behavior during tests. <br>One way to do this is to specify a
function’s return value.

1. create a file called my_calendar.py. Add is_weekday(), a function that uses Python’s datetime library to determine
   <br>whether today is a week day. Finally, write a test that asserts that the function works as expected

```python
from datetime import datetime


def is_weekday():
    today = datetime.today()
    # Python's datetime library treats Monday as 0 and Sunday as 6
    return (0 <= today.weekday() < 5)


# Test if today is a weekday
assert is_weekday()
```

2. Since you’re testing if today is a weekday, the result depends on the day you run your test
3. When writing tests, it is important to ensure that the results are <span style="color:#00FF00">
   predictable</span> <br>You can use Mock to eliminate uncertainty from your code during testing.

```python
import datetime
from unittest.mock import Mock

# Save a couple of test days
tuesday = datetime.datetime(year=2019, month=1, day=1)
saturday = datetime.datetime(year=2019, month=1, day=5)

# Mock datetime to control today's date
datetime = Mock()


def is_weekday():
    today = datetime.datetime.today()
    # Python's datetime library treats Monday as 0 and Sunday as 6
    return (0 <= today.weekday() < 5)


# Mock .today() to return Tuesday
datetime.datetime.today.return_value = tuesday
# Test Tuesday is a weekday
assert is_weekday()
# Mock .today() to return Saturday
datetime.datetime.today.return_value = saturday
# Test Saturday is not a weekday
assert not is_weekday()
```

### Managing a Mock’s Side Effects

1. You can <span style="color:#00FF00">control your code’s behavior</span> by specifying a mocked function’s side
   effects. <br>A .side_effect defines what happens when you call the mocked function.

```python
import requests


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None
```

2. You can test how get_holidays() will respond to a connection timeout by setting requests.get.side_effect.

```python
import unittest
from requests.exceptions import Timeout
from unittest.mock import Mock

# Mock requests to control its behavior
requests = Mock()


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None


class TestCalendar(unittest.TestCase):
    def test_get_holidays_timeout(self):
        # Test a connection timeout
        requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_holidays()
```

3. .side_effect can also be an iterable. The iterable must consist of return values, exceptions, or a mixture of both.

```python
import unittest
from requests.exceptions import Timeout
from unittest.mock import Mock

# Mock requests to control its behavior
requests = Mock()


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None


class TestCalendar(unittest.TestCase):
    def test_get_holidays_retry(self):
        # Create a new Mock to imitate a Response
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            '12/25': 'Christmas',
            '7/4': 'Independence Day',
        }
        # Set the side effect of .get()
        requests.get.side_effect = [Timeout, response_mock]
        # Test that the first request raises a Timeout
        with self.assertRaises(Timeout):
            get_holidays()
        # Now retry, expecting a successful response
        assert get_holidays()['12/25'] == 'Christmas'
        # Finally, assert .get() was called twice
        assert requests.get.call_count == 2


if __name__ == '__main__':
    unittest.main()
```

### Configuring Your Mock

1. You can configure a Mock to set up some of the object’s behaviors. Some configurable members include <br>
   .side_effect, .return_value, and .name. You configure a Mock when you <span style="color:#00FF00">create</span> one
   or when you use <span style="color:#00FF00">.configure_mock()</span>.
2. While .side_effect and .return_value can be set on the Mock instance, itself, other attributes like
   .name <br><span style="color:#FFA500">can only be set through .__init__() or .configure_mock()</span>

```python
mock = Mock(name='Real Python Mock')
mock.name
# < Mock name = 'Real Python Mock.name' id = '4434041544' >

mock = Mock()
mock.name = 'Real Python Mock'
mock.name
# 'Real Python Mock'
```

3. You can configure an existing Mock using .configure_mock()

```python
mock = Mock()
mock.configure_mock(return_value=True)
mock()
# True

# Verbose, old Mock
response_mock = Mock()
response_mock.json.return_value = {
    '12/25': 'Christmas',
    '7/4': 'Independence Day',
}

# Shiny, new .configure_mock()
holidays = {'12/25': 'Christmas', '7/4': 'Independence Day'}
response_mock = Mock(**{'json.return_value': holidays})
```

### patch()

unittest.mock provides a powerful mechanism for mocking objects, called patch(), <br>which looks up an object in a given
module and replaces that object with a Mock

#### path() as a Decorator

1. If you want to mock an object for the duration of your entire test function, <br>you can use patch() as a function
   decorator.
2. To see how this works, reorganize your my_calendar.py file by putting the logic and tests into separate files

```python
import requests
from datetime import datetime


def is_weekday():
    today = datetime.today()
    # Python's datetime library treats Monday as 0 and Sunday as 6
    return (0 <= today.weekday() < 5)


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None
```

2. These functions are now in their own file, separate from their tests. <br>Next, you’ll re-create your tests in a file
   called test_my_calendar.py

```python
import unittest
from my_calendar import get_holidays
from requests.exceptions import Timeout
from unittest.mock import patch


class TestCalendar(unittest.TestCase):
    @patch('my_calendar.requests')
    def test_get_holidays_timeout(self, mock_requests):
        mock_requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_holidays()
            mock_requests.get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
```

3. Originally, you created a Mock and patched requests in the local scope. <br>Now, you need to access the requests
   library in my_calendar.py from test_my_calendar.py.

#### patch() as a Context Manager

1. Sometimes, you’ll want to use patch() as a context manager rather than a decorator
    1. You only want to mock an object for a part of the test scope
    2. You are already using too many decorators or parameters, which hurts your test’s readability.

```python
import unittest
from my_calendar import get_holidays
from requests.exceptions import Timeout
from unittest.mock import patch


class TestCalendar(unittest.TestCase):
    def test_get_holidays_timeout(self):
        with patch('my_calendar.requests') as mock_requests:
            mock_requests.get.side_effect = Timeout
            with self.assertRaises(Timeout):
                get_holidays()
                mock_requests.get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
```

### Patching an Object's Attribute

1. Let’s say you only want to mock one method of an object instead of the entire object. <br>You can do so by using
   patch.object()

```python
import unittest
from my_calendar import requests, get_holidays
from unittest.mock import patch


class TestCalendar(unittest.TestCase):
    @patch.object(requests, 'get', side_effect=requests.exceptions.Timeout)
    def test_get_holidays_timeout(self, mock_requests):
        with self.assertRaises(requests.exceptions.Timeout):
            get_holidays()


if __name__ == '__main__':
    unittest.main()
```

### Where to Patch

1. Knowing where to tell patch() to look for the object you want mocked is important
2. Let’s say you are mocking is_weekday() in my_calendar.py using patch()

```python
# Good
import my_calendar
from unittest.mock import patch

with patch('my_calendar.is_weekday'):
    my_calendar.is_weekday()

# Bad
from my_calendar import is_weekday
from unittest.mock import patch

with patch('my_calendar.is_weekday'):
    is_weekday()
```

3. Even though you patched my_calendar.is_weekday, is_weekday() is different
4. The difference is due to the change in how you imported the function
5. from my_calendar import is_weekday binds the real function to the local scope. <br>So, even though you patch() the
   function later, you <span style="color:#FFA500">ignore the mock</span> because you already have a local reference to
   the un-mocked function <br>
6. A good rule of thumb is to patch() the object <span style="color:#00FF00">where it is looked up</span>.
7. In the first example, mocking 'my_calendar.is_weekday()' works because you look up the function in the my_calendar
   module
8. In the second example, you have a local reference to is_weekday(). <br>Since you use the function found in the local
   scope, <span style="color:#FFA500">you should mock the local function</span>

```python
from unittest.mock import patch
from my_calendar import is_weekday

with patch('__main__.is_weekday'):
    is_weekday()
```
