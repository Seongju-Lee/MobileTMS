# 레디엔터테인먼트 모델 검색 플랫폼

100,000명의 모델정보, 진행 광고건, 광고 일정을 외부에서 확인하기 위한 플랫폼  <br/>
카카오 엔터테인먼트의 공동개발 플랫폼인 TMS의 모바일 버전

<img src="https://img.shields.io/badge/Python3.8-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/FastAPI 0.78.0-009688?style=flat-square&logo=FastAPI&logoColor=white"/>

## How to?
- <b>backend/Scripts</b>
- <b>run activate</b>
  - MAC: source ./activate
  - Windows: .\activate
- <b>cd backend</b>
- <b>uvicorn 실행</b>
  - uvicorn main:app --reload

## swagger
host/docs 통해서 api 설계 확인 가능. <br/>
(관련폴더: /backend/apis)

## DB관련 폴더
- <b>backend/db</b>: db connect 및 기능별 폴더
- <b>backend/db/repository</b>: ORM Queries
- <b>그 외</b>: 기능별 테이블 정의 클래스

## 페이지 렌더 관련
- <b>/backend/webapps</b>: router 폴더(html 렌더링)

## Dockerfile
- DockerImage 생성 코드(서버 내 사용)

## gitignore
- env 파일
- model.json
- api관련 파일
