
# AWS CDK demo [Tibia char info web-scraping].

* _AWS Services_: `Api Gateway`, `Lambda`, `DynamoDB`.
* _Goals_:
  * Management (_CRUD_) of tibia's char info.
* _Docs_:
  * `cdk.json` might be using wrong python's bin file version.
  * GET/POST/DELETE <rest_api_url>/char/{charname}
  * Slides: [Google Drive](https://docs.google.com/presentation/d/1JkRvEB96tWdElryMJNMWi57lgWHQHFJB/edit?usp=sharing&ouid=107633070004175527539&rtpof=true&sd=true)
* _Reqs_:
  * _Py_ [**==3.8**]

### Usage

- `cdk bootstrap` [_once only_]
- `cdk synth [--profile <profile_name]`
- `cdk deploy --app "cdk.out/<assembly templates dir>" [--profile <profile_name]` 
* **Options**:
  * specify whether to use **chalice** or not [at _app.py_ -> _TibiaCharsManagement's_ **_chalice_app: bool_** parameter]