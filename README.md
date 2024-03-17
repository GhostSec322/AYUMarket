# AYUMarket
### [2024] AYUMarket 쇼핑몰 제작
본 프로젝트는 쇼핑몰을 제작하는 프로젝트 입니다 아래와 같은 기술을 사용하여 기능을 구현합니다 
### Skill
| Language | Framework | API | DBMS | library|
|----------|-----------|-----|------|------|
| ![Python Badge](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) ![HTML Badge](https://img.shields.io/badge/-HTML-E34F26?style=flat&logo=html5&logoColor=white) ![CSS Badge](https://img.shields.io/badge/-CSS-1572B6?style=flat&logo=css3&logoColor=white) ![JavaScript Badge](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) ![SQL Badge](https://img.shields.io/badge/-SQL-4479A1?style=flat&logo=sql&logoColor=white) | ![Django Badge](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white) | ![API Badge](https://img.shields.io/badge/-Iamport%20API-009688?style=flat) <br> ![API Badge](https://img.shields.io/badge/-Delivery%20Tracker%20API-009688?style=flat) ![Kakao Login Badge](https://img.shields.io/badge/-Kakao%20Login-FFCD00?style=flat&logo=kakao&logoColor=black) ![Google Login Badge](https://img.shields.io/badge/-Google%20Login-4285F4?style=flat&logo=google&logoColor=white) | ![MySQL Badge](https://img.shields.io/badge/-MySQL-4479A1?style=flat&logo=mysql&logoColor=white) |![Chart.js Badge](https://img.shields.io/badge/-Chart.js-FF6384?style=flat&logo=chart.js&logoColor=white)|

### 기능
#### 1. 회원가입, 로그인
- 해당 기능은 Email, Password ,사용자 이름을 필요로 하게 되며 google와kakao에서 제공하는 api를 이용하여 로그인 하는 기능또한 포함하게 됩니다. 
#### 2. 상품 등록 
- 이 기능은 허가된 사용자만 상품을 등록할 수 있습니다 
- 이때 상품이미지,재고, 가격 , 상세 설명을 판매자로부터 입력을 받아야 하며 Null을 허용하지 않습니다. 
#### 3. 판매자 데시보드 
- 판매자가 올린 상품에 대하여 판매와 관련된 통계를 제공합니다 그리고 주문목록, 문의사항등에 대하여 보여주게 되며 결제 취소기능을 포함 합니다 
#### 4.검색
- 사용자에게 상품을 검색할 수 있는 기능과 카테고리별 상품을 보여주는 기능을 포함하고 있습니다. 
#### 5. 배송조회 
- Develivery Tracker API를 이용하여 사용자가 배송조회를 할 시 현재 배송상태를 보여주게 됩니다.

##### 6. 장바구니 
- 사용자는 물건을 장바구니에 담을 수 있으며 향후 일괄 결제를 할 수 있습니다.

#### 7. 리뷰 기능
- 사용자는 상품에 대하여 리뷰를 남길 수 있습니다.

#### 8. 환불기능
- 사용자의 요청에 따라 환불요청을 할 수 있습니다. 
