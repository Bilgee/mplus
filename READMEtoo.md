# API tailbar

## Available APIs
> /v1.0/topicmodel/en   ## used for english magazines 
## Available languages

available languages for topic extraction: English (en), Japanese (ja), Chinese Simplified (zh or zh-cn), Chinese Traditional (zh-tw), Russian (ru), Indonesian (id), Malay (ms), Mongolian (mn)

available languages for NER: [102 languages](https://github.com/google-research/bert/blob/master/multilingual.md#list-of-languages) (bert multilingual)

available languages for keyword extraction: usable on any text

## Example output:

    "response": {
        "code": 0,
        "text": [
            {
                "Topic": [ ### top 2 found topic
                    {
                        "Score": 0.145, ### confidence score, if score is below 0.1, it's recommended to ignore the category 
                        "Category": "Business & News", ### Category of the topic
                        "Words": [  ### top words that describe this topic
                            {
                                "Text": "sg",
                                "Score": 0.123
                            },
                            ...]
                    },{
                        "Score": 0.131,
                        "Category": "Travel and Culture",
                        "Words": [...],
                    }]
                "Named Entity": [ ### Found named entities
                    {
                        "Text": "CASA",
                        "Label": "ORG"
                    },{
                        "Text": "Jakarta",
                        "Label": "GPE"
                    },{
                        "Text": "MRA_Media_Photography_Department",
                        "Label": "ORG"
                    }
                ]
            },... ##### other pages 
        ]
    }
> "code": 0 is success, 1 is error

> "Topic" - Most relevant 2 topics

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

> **Note:** Named entities with more than 1 words has "_" (underscore) bewteen them. (i.e. `MRA_Media_Photography_Department`, `H_._B_._Putra`)

## Example input json

    {
    "data": [{
        "path": "0001/index.html",
        "image": "0001/0/1.jpg",
        "page_number": 1,
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
        ]
    }

> Used tags in text analyzing ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'bold', 'italic', 'text']