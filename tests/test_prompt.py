from explainer.prompt import build_prompt

my_python_func = """def add_to_even(numbers: list[int]):
        return [number + 1 for number in numbers if number % 2 == 0]"""

my_js_func = """const subtract_from_odd = (numbers) => {
      return numbers.map(number => {
        if (number % 2 !== 0) {
          return number - 1;
        }
        return number
      })
    } """


def test_build_prompt_with_language_and_question():
    prompt_1 = build_prompt(my_python_func, "python", "Is this code performant?")
    assert prompt_1 == (
        "The following is written in python.\n\n"
        "Answer this question about the code: Is this code performant?\n\n"
        f"```\n{my_python_func}\n```"
    )


def test_build_prompt_without_question():
    prompt_2 = build_prompt(my_js_func, "js")
    assert prompt_2 == (
        "The following is written in js.\n\n"
        "Explain what this code does. Be concise and clear.\n\n"
        f"```\n{my_js_func}\n```"
    )


def test_build_prompt_without_language():
    prompt_3 = build_prompt(my_js_func)
    assert prompt_3 == (
        "The following is source code.\n\n"
        "Explain what this code does. Be concise and clear.\n\n"
        f"```\n{my_js_func}\n```"
    )
