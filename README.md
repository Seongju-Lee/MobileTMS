# 레디엔터테인먼트 모델 검색 플랫폼

100,000명의 모델정보, 진행 광고건, 광고 일정을 외부에서 확인하기 위한 플랫폼  <br/>
카카오 엔터테인먼트의 공동개발 플랫폼인 TMS의 모바일 버전

## How to?
- backend/Scripts 접근
- 'backend' 가상환경 실행
  - MAC: source ./activate
  - Windows: .\activate
- backend 디렉터리로 이동 후
- uvicorn 실행
  - uvicorn main:app --reload

## gitignore
- env 파일
- model.json
- api관련 파일

## swagger
host/docs 통해서 api 설계 확인 가능. <br/>
(관련폴더: /backend/apis)

## DB관련 폴더
- backend/db: db connect 및 기능별 폴더
- backend/db/repository: ORM Queries
- 그 외: 기능별 테이블 정의 클래스

## 페이지 렌더 관련
- /backend/webapps: router 폴더(html 렌더링 해주는 폴더)

## Dockerfile
- DockerImage 생성 코드 (서버 내 사용)