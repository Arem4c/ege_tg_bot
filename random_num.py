import random
#Генерирует случайное целое число от 0 до a (включительно)
def random_number():
    result = random.randint(0, 10)
    return str(result)
