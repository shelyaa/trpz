from abc import ABC


class Condition(ABC):
    pass


class TermainalCondition(Condition):

    def __init__(self, v1, v2):
        self.v1, self.v2 = v1, v2


class NonTerminalCondition(Condition):

    def __init__(self, *conditions):
        self.conditions = conditions


class EqCondition(TermainalCondition):

    def __bool__(self):
        return self.v1 == self.v2


class NeCondition(TermainalCondition):

    def __bool__(self):
        return self.v1 != self.v2


class GtCondition(TermainalCondition):

    def __bool__(self):
        return self.v1 > self.v2


class GeCondition(TermainalCondition):

    def __bool__(self):
        return self.v1 >= self.v2


class LtCondition(TermainalCondition):

    def __bool__(self):
        return self.v1 < self.v2


class LeCondition(TermainalCondition):

    def __bool__(self):
        return self.v1 <= self.v2
    

class OrCondition(NonTerminalCondition):

    def __bool__(self):
        return any(self.conditions)


class AndCondition(NonTerminalCondition):
    
    def __bool__(self):
        return all(self.conditions)


class Interpreter:

    conditions = {
        'eq': EqCondition,
        'ne': NeCondition,
        'gt': GtCondition,
        'ge': GeCondition,
        'lt': LtCondition,
        'le': LeCondition,
        'or': OrCondition,
        'and': AndCondition
    }

    def __init__(self, condition):
        self.__condition = condition

    def __eval(self, operator, value):

        if issubclass(Interpreter.conditions[operator], TermainalCondition):
            
            if not isinstance(value, list):
                raise TypeError(f"Invalid condition. Value for \"{operator}\" operator must be list.")
            
            if len(value) != 2:
                raise ValueError(f"Invalid condition. Value for \"{operator}\" operator must contain two values.")
            
            return Interpreter.conditions[operator](*value)
        
        elif issubclass(Interpreter.conditions[operator], NonTerminalCondition):

            if not isinstance(value, dict):
                raise TypeError(f"Invalid condition. Value for \"{operator}\" operator must be dictionary.")
            
            return Interpreter.conditions[operator](*[self.__eval(op, val) for op, val in value.items()])

    def __bool__(self):

        try:

            initial_operator = list(self.__condition.keys())[0]

            return bool(self.__eval(initial_operator, self.__condition[initial_operator]))
        
        except KeyError as exception:
            raise Exception(f"Invalid condition. Operator {exception} is not supported.")
