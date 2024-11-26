def convert_text_block(block):
    """Convert a text block to HTML"""
    text = block.get('text', '')
    block_type = block.get('type', 'paragraph')
    
    if block_type == 'heading-1':
        return f'<h1>{text}</h1>'
    elif block_type == 'heading-2':
        return f'<h2>{text}</h2>'
    else:
        return f'<p>{text}</p>'

def convert_table_block(table_block):
    """Convert a table block to HTML"""
    html = ['<table border="1">']
    
    for row in table_block.get('bodyRows', []):
        html.append('<tr>')
        for cell in row.get('cells', []):
            colspan = f' colspan="{cell["colSpan"]}"' if cell.get('colSpan', 1) > 1 else ''
            rowspan = f' rowspan="{cell["rowSpan"]}"' if cell.get('rowSpan', 1) > 1 else ''
            
            html.append(f'<td{colspan}{rowspan}>')
            for block in cell.get('blocks', []):
                if 'textBlock' in block:
                    html.append(convert_text_block(block['textBlock']))
            html.append('</td>')
        html.append('</tr>')
    
    html.append('</table>')
    return '\n'.join(html)

def convert_blocks(blocks):
    """Recursively convert blocks to HTML"""
    html = []
    
    for block in blocks:
        if 'textBlock' in block:
            html.append(convert_text_block(block['textBlock']))
            # Handle nested blocks
            if 'blocks' in block['textBlock']:
                html.append(convert_blocks(block['textBlock']['blocks']))
        elif 'tableBlock' in block:
            html.append(convert_table_block(block['tableBlock']))
    
    return '\n'.join(html)

def convert_json_to_html(json_doc):
    """Convert the JSON document to HTML"""
    html = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="UTF-8">',
        '<title>Court Document</title>',
        '<style>',
        'body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }',
        'table { border-collapse: collapse; width: 100%; margin: 15px 0; }',
        'td { padding: 8px; }',
        'h1 { color: #2c3e50; }',
        'h2 { color: #34495e; }',
        '</style>',
        '</head>',
        '<body>'
    ]
    
    # Convert document blocks
    blocks = json_doc.get('documentLayout', {}).get('blocks', [])
    html.append(convert_blocks(blocks))
    
    html.append('</body>')
    html.append('</html>')
    
    return '\n'.join(html)

def save_html(json_doc, output_file='output.html'):
    """Save the HTML to a file"""
    html_content = convert_json_to_html(json_doc)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Example usage:
if __name__ == '__main__':
    import json
    
    # Read JSON file
    with open('document.json', 'r', encoding='utf-8') as f:
        document = json.load(f)
    
    # Convert and save to HTML
    save_html(document)
    print("HTML file has been generated as 'output.html'") 