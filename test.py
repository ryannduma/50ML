def say_hello(n):
    if n > 0:
        print("Hello, World!")
        say_hello(n - 1)

say_hello(15)