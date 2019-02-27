# Documentation

## 1. ```/api/spider```

- description: 爬虫接口，增量爬取数据
- method: ```POST```
- headers: ```authorized:<authorized-keys>```
- rtype: ```json```
```
{
    "code": 200,
    "data": "OK"
}
```

## 2. ```/api/add_category```

- description: 新增文章分类
- method: ```POST```
- form-data: 
```
category_id:<category_id>
category_name:<category_name>
```
- rtype: ```json```
```
{
    "code": 200,
    "data": "OK"
}
```

## 3. ```/api/article_list```

- description: 获取文章列表
- method: ```GET```
- parameter: 
```
category_id:<category_id> default 0
limit:<max items> default 50
```
- rtype: ```json```
```
{
    "code": 200,
    "data": [
        {
            "id": <id>,
            "title": <title>,
            "date": <date>,
            "author_avatar": <article_cover>,
            "category": <category>
        },
        {
            "id": <id>,
            "title": <title>,
            "date": <date>,
            "author_avatar": <article_cover>,
            "category": <category>
        }
    ]
}
```

## 4. ```/api/article/<article_id>```

- description: 获取文章
- method: ```GET```
- rtype: ```json```
```
{
    "code": 200,
    "data": [
        {
            "id": <id>,
            "title": <title>,
            "date": <date>,
            "source": <source>,
            "author_avatar": <author_avatar>,
            "editor": <editor>,
            "content": <content>,
            "category":{
                "id": <category_id>,
                "display_name": <name>
            }
        },
        {
            "id": <id>,
            "title": <title>,
            "date": <date>,
            "source":<source>,
            "author_avatar":<author_avatar>,
            "editor":<editor>,
            "content": <content>,
            "category":{
                "id":<category_id>,
                "display_name":<name>
            }
        }
    ]
}
```
