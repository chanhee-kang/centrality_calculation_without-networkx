# Title / Centrality_Calculation
route.csv 내의 centrality를 계산하는 코드 입니다

## Installation
Python 3.x 환경에서 작성 하였습니다.
각 패키지를 pip명령어를 통해 설치하여 주십시오.

## Explaination
Route.csv 파일은 공항에서 공항의 경로를 표시해준 csv파일입니다
AFK -> ARE 공항으로 이동시 각각의 betweenness, clossness, 및 degree centrality를 계산하여 줍니다.

## Usage
* step1: main.py를 사용하여 betweenness, clossness, 및 degree centrality를 계산합니다.
* step2: network_centralization_based.py를 사용하여  network_centralization_based를 계산합니다.

## Limitations
multiprocessing을 추가하여도 속도면에서 느립니다
matrix 형태로 problem solving 방면으로 다시 구축 

## Contact
작동에 문제가 생기시거나 궁금한점이 있으시면 연락주시면 감사하겠습니다 [https://ck992.github.io/](https://ck992.github.io/).
