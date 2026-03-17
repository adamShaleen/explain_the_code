def build_prompt(
    code: str, language: str | None = None, question: str | None = None
) -> str:
    language_hint = (
        f"The following is written in {language}."
        if language
        else "The following is source code."
    )

    if question:
        task = f"Answer this question about the code: {question}"
    else:
        task = "Explain what this code does. Be concise and clear."

    return f"{language_hint}\n\n{task}\n\n```\n{code}\n```"
