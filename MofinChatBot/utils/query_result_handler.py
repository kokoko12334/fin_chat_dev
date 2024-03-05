def process_query_result(res):
    count = 0
    for m in res['matches']:
        count += m['metadata']['result']
    
    percent = count/len(res['matches'])
    signal = 0 if percent < 0.5 else 1
    percent = 1 - percent if percent < 0.5 else percent
    # table = create_markdown_table(count, len(res['matches']))
    return percent* 100, signal

def create_markdown_table(count, total_count):
    data = {"상태": ["올랐음", "떨어짐"], "개수": [count/total_count*100, (total_count - count)/total_count * 100]}
    table = "## 주식 Query 결과\n\n"
    table += "| 상태   | 확률 |\n"
    table += "|--------|------|\n"
    for i in range(len(data['상태'])):
        table += f"| {data['상태'][i]} | {data['개수'][i]} |\n"
    return table