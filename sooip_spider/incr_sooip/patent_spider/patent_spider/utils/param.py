def list_param(date, start=1):
    data = {
        "secondKeyWord": "名称+摘要+主权项",
        "secondkeyWordVal": "",
        "secondSearchType": "AND",
        "attribute-node:patent_cache-flag": "false",
        "attribute-node:patent_start-row": str(start),
        "attribute-node:patent_page-row": "50",
        "attribute-node:patent_sort-column": "ano",
        "attribute-node:patent_page": "1",
        "express2": "",
        "express": "(公开（公告）日 =  ( %s ) )" % date,
        "isFamily": "",
        "categoryIndex": "",
        "selectedCategory": "",
        "patentLib": "pdb = 'CNA0' OR pdb = 'CNB0' OR pdb = 'CNY0' OR pdb = 'CNS0' OR pdbc ='HK' OR pdbc ='MO' OR pdbc ='TW'",
        "patentType": "patent2",
        "order": "",
        "pdbt": "",
    }
    return data