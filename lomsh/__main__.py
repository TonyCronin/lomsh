try:
    from .cli import main
except ImportError:
    from lomsh.cli import main

main()
