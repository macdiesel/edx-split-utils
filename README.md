Hackathon X split-utils project
# Hackathon X split-utils

## Getting Started:
pip install -r requirements.txt

python run.py

## Examples:

### Get history:
```
curl "http://localhost:5000/api/v1/history/main/course-v1:edX+test105+2015_Q2"

["55b138a556c02c5da9b2e189", "55b1396856c02c5da9b2e18d", "55b139a956c02c5da9b2e9d1"]%

```

### Get the graph:
 ```
 curl "http://localhost:5000/api/v1/history/all/course-v1:edX+test105+2015_Q2"

{
    "55b139a956c02c5da9b2e9d1": [],
    "55b138a556c02c5da9b2e189": [
        "55b1396856c02c5da9b2e18d"
    ],
    "root": [
        "55b138a556c02c5da9b2e189"
    ],
    "55b1396856c02c5da9b2e18d": [
        "55b139a956c02c5da9b2e9d1"
    ]
}
 ```

### Get block counts:
```
curl "http://localhost:5000/api/v1/block_counts/course-v1:edX+test105+2015_Q2"

{
    "chapter": 7,
    "course_info": 2,
    "about": 5,
    "vertical": 97,
    "discussion": 7,
    "static_tab": 3,
    "html": 118,
    "course": 1,
    "sequential": 28,
    "video": 21,
    "word_cloud": 1,
    "problem": 4
}
```

### Get structure ID:
```
curl "http://localhost:5000/api/v1/structure_id/course-v1:edX+test105+2015_Q2"

{"$oid": "55b139a956c02c5da9b2e9d1"}
```