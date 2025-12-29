import pytest 
from unittest.mock import patch 
from io import StringIO

from src.newmain import is_field_valid, is_quit, main

def test_main_with_field_valid():
    """Test main() with a valid expense name."""
    with patch('builtins.input', return_value='Groceries'):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "Expense name entered: Groceries" in output

def test_main_with_quit_command():
    """Test main() with quit command."""
    with patch('builtins.input', return_value='quit'):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            assert "Exiting input." in output
            assert "Expense name entered: quit" not in output 
    