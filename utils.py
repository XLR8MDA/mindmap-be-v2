def convert_to_markdown(raw_text: str) -> str:
    lines = raw_text.split('\n')
    markdown_lines = []
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line:
            # Count the number of leading '#' to determine heading level
            heading_level = len(line) - len(stripped_line)
            # Ensure heading level is between 1 and 6
            heading_level = min(max(heading_level, 1), 6)
            # Construct the markdown heading
            markdown_line = f"{stripped_line}"
            markdown_lines.append(markdown_line)
    return "\n".join(markdown_lines)
