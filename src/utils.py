# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

def y_or_n_pred(question, default=None):
    """Print '<question>? [y/n]' on stdout and ask for a y/n answer.

    Returns a boolean.

    Parameters:
    question --
    default  -- the value to return if no answer is given. If None, ask again.
    """
    print("{}? [{}/{}]"
          .format(question,
                  ("Y" if default is True else "y"),
                  ("N" if default is False else "n")))

    answer = input()

    if answer == "y" or answer == "Y":
        return True
    elif answer == "n" or answer == "N":
        return False
    elif default is None:
        print("Please answer y or n. ")
        return y_or_n_pred(question, None)
    else:
        return default

def find_minimizing_with_rating(lst, rating_fn):
    """Find the element in lst minimizing rating_fn(elememt).

    Returns a pair of the element of lst and its rating.
    When multiple elements minimizing the rating exist,
    returns a pair of the first such element and its rating

    Parameters:
    lst       -- The list of elements
    rating_fn -- The rating function. Assigns a value that can be compared by '<'
    """
    (min_val, min_rating) = (None, None)
    for el in lst:
        rating = rating_fn(el)
        if min_rating is None or rating < min_rating:
            (min_val, min_rating) = (el, rating)
    return (min_val, min_rating)

def find_minimizing(lst, rating_fn):
    """Find the element in lst minimizing rating_fn(elememt).

    Returns the element of lst.
    When multiple elements minimizing the rating exist,
    returns the first such element

    Parameters:
    lst       -- The list of elements
    rating_fn -- The rating function. Assigns a value that can be compared by '<'
    """
    (res, _) = find_minimizing_with_rating(lst, rating_fn)
    return res
