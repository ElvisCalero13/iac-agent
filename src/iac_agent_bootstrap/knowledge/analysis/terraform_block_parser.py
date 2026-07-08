def extract_terraform_block(content: str, start: int) -> str | None:
    index = content.find("{", start)

    if index == -1:
        return None

    depth = 0

    while index < len(content):
        char = content[index]

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1

            if depth == 0:
                return content[start:index + 1]

        index += 1

    return None
