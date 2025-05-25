def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        
        for i, (arg_name, arg_type) in enumerate(annotations.items()):
            if arg_name == 'return':
                continue
                
            if i < len(args):
                if not isinstance(args[i], arg_type):
                    raise TypeError(f"Аргумент '{arg_name}' должен быть типа {arg_type.__name__}")
            elif arg_name in kwargs:
                if not isinstance(kwargs[arg_name], arg_type):
                    raise TypeError(f"Аргумент '{arg_name}' должен быть типа {arg_type.__name__}")
        
        return func(*args, **kwargs)
    return wrapper
