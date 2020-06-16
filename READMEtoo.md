# API tailbar

# install
```shell
pip install --upgrade -r requirements.txt
python -m deeppavlov install ner_ontonotes_bert_mult
```
## to use it on japanese
for smaller tokenizer
```shell
pip install 'fugashi[unidic-lite]'
```
full version
```shell
pip install 'fugashi[unidic]'
python -m unidic download
```
## to use it on chinese
```shell
pip install jieba
```
## Available APIs
> /v1.0/topicmodel/en   ##used for extracting information from magazines 

> /v1.0/ad/en       ##used for matching ads with magazine content
## Available languages

available languages for topic extraction: English (en), Japanese (ja), Chinese Simplified (zh or zh-cn), Chinese Traditional (zh-tw), Russian (ru), Indonesian (id), Malay (ms), Mongolian (mn)

available languages for NER: [102 languages](https://github.com/google-research/bert/blob/master/multilingual.md#list-of-languages) (bert multilingual)

available languages for keyword extraction: usable on any text

[language codes](https://poeditor.com/docs/languages)

# /v1.0/topicmodel/en - details

## Example input json

    {
    "data": [{
        "path": "0001/index.html",
        "image": "0001/0/1.jpg",
        "page_number": 0,
        "title": "PLAYWORKS",
        "h1": [],
        "h2": ["PLAYWORKS"],
        "h3": [],
        "h4": ["PT. Cordialels Sistem Furniture"],
        "h5": ["www.globalfursys.com"],
        "span": [],
        "bold": [],
        "italic": [],
        "text": ["PLAYWORKS breaks down the boundaries between rest and work space, adding communication and concentration.", "Intiland Tower, 9th Floor| Jl. Jendral Sudirman 32 Jakarta 10220 IndonesiaPhone : +62 812 8544 3375 / +62 813 2062 041| Email 1 : sinat@cordialels.com| Email 2 : sales@cordialels.com"]
        },... ##more pages if necessary
        ],
        "lang": "en"
    }

> Used tags in text analyzing ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'bold', 'italic', 'text']

>[language codes](https://poeditor.com/docs/languages) to write in "lang" field

## Example output:

    "response": {
        "code": 0,
        "text": [
            {
                "topic": [ ### top 2 found topic
                    {
                        "score": 0.145, ### confidence score, if score is below 0.1, it's recommended to ignore the category 
                        "category": "Business & News", ### Category of the topic
                        "words": [  ### top words that describe this topic
                            {
                                "text": "sg",
                                "score": 0.123
                            },
                            ...]
                    },{
                        "score": 0.131,
                        "category": "Travel and Culture",
                        "words": [...],
                    }]
                "named entity": [ ### Found named entities
                    {
                        "text": "CASA",
                        "label": "ORG"
                    },{
                        "text": "Jakarta",
                        "label": "GPE"
                    },{
                        "text": "MRA_Media_Photography_Department",
                        "label": "ORG"
                    }
                ],
                "keywords": [
                    "playworks"
                ],
                "page_number": 0
            },... ##### other pages 
        ]
    }
> "code": 0 is success, 1 is error

> "topic" - Most relevant 2 topics

> **Note:** About topic's score - if score is below 0.1, it's recommended to ignore that topic/category

## NER - Named Entity Recognizer
|Label | description |
|------|-------------|
| NORP | Nationalities or religious or political groups |
| FAC |Buildings, airports, highways, bridges, etc.|
| ORG |Companies, agencies, institutions, etc. |
| GPE |Countries, cities, states |
| LOC |Non-GPE locations, mountain ranges, bodies of water |
| PRODUCT | Vehicles, weapons, foods, etc. (Not services) |
| EVENT | Named hurricanes, battles, wars, sports events, etc. |
| WORK_OF_ART | Titles of books, songs, etc. |
| LAW | Named documents made into laws |
| LANGUAGE | Any named language |

> **Note:** Named entities with more than 1 words has "_" (underscore) between them. (i.e. `MRA_Media_Photography_Department`, `H_._B_._Putra`)

# /v1.0/ad/en - details

## Example input json

    {
        "data": {
            "ad": [
                {
                    "id": 54,
                    "lang": "ja",
                    "words": [
                        "相撲",
                        "レスリング",
                        "お父さん",
                        "授業",
                        "強い"
                    ]
                },
                {
                    "id": 53,
                    "lang": "en",
                    "words": [
                        "watch",
                        "collection",
                        "blancpain",
                        "wristwatch",
                        "women"
                    ]
                }
            ],
            "magazines": [
                {
                    "id": "Women,weekly",
                    "pages": [
                        {
                            "topic": [
                                {
                                    "category": "Business & News",
                                    "score": 0.1931,
                                    "words": [
                                        {
                                            "text": "management",
                                            "score": 0.1795
                                        },
                                        {
                                            "text": "manager",
                                            "score": 0.1458
                                        },
                                        ...
                                    ],
                                    "index": 211
                                },
                                {
                                    "category": "Business & News",
                                    "score": 0.1353,
                                    "words": [
                                        {
                                            "text": "director",
                                            "score": 0.0801
                                        },
                                        {
                                            "text": "board",
                                            "score": 0.0474
                                        },
                                        ...
                                    ],
                                    "index": 184
                                }
                            ],
                            "named entity": [
                                {
                                    "text": "Alice_Rappa",
                                    "label": "PERSON"
                                },
                                {
                                    "text": "Singapore",
                                    "label": "GPE"
                                },
                                ...
                            ],
                            "keywords": [
                                "Director",
                                "Editor",
                                "Head",
                                "Account",
                                "Circulation",
                                "Senior"
                            ],
                            "page_number": 6
                        },
                        ...
                    ]
                },
                {
                    "id": "japan sumo",
                    "pages": [
                        {
                            "topic": [
                                {
                                    "category": "unknown",
                                    "score": 0,
                                    "words": [
                                        {
                                            "text": "",
                                            "score": 0
                                        }
                                    ]
                                }
                            ],
                            "named entity": [
                                {
                                    "text": "",
                                    "label": ""
                                }
                            ],
                            "keywords": [
                                "画像",
                                "表紙",
                                ""
                            ],
                            "page_number": 0
                        },
                    ...
                    ]
                }
            ]
        }
    }

>[language codes](https://poeditor.com/docs/languages) to write in "lang" field

## Example output:

    {
        "response": {
            "code": 0,
            "text": [
                {
                    "magazine_id": "Women,weekly",
                    "ad_match": [
                        {
                            "ad_page_match": [],
                            "ad_number": 54
                        },
                        {
                            "ad_page_match": [
                                {
                                    "score": 0.17353,
                                    "page_number": 90,
                                    "magazine_id": "Women,weekly"
                                }
                            ],
                            "ad_number": 53
                        }
                    ]
                },
                {
                    "magazine_id": "japan sumo",
                    "ad_match": [
                        {
                            "ad_page_match": [
                                {
                                    "score": 0.60004,
                                    "page_number": 8,
                                    "magazine_id": "japan sumo"
                                },
                                {
                                    "score": 0.40978,
                                    "page_number": 37,
                                    "magazine_id": "japan sumo"
                                },
                                {
                                    "score": 0.40313,
                                    "page_number": 24,
                                    "magazine_id": "japan sumo"
                                },
                                {
                                    "score": 0.40309,
                                    "page_number": 14,
                                    "magazine_id": "japan sumo"
                                }
                            ],
                            "ad_number": 54
                        },
                        {
                            "ad_page_match": [],
                            "ad_number": 53
                        }
                    ]
                }
            ]
        }
    }
> "code": 0 is success, 1 is error

> for each magazine and ad pairs, api returns up to 10 possible matches

> api creates a topic model for ads then matches the topics with the magazine topics. 
Also checks for exact keyword match with named entities and keywords of the magazine.