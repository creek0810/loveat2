# README

---

[TOC]

---

## 分工
  - SRS: 全員
  - SDD: 全員
  - STD: 李萱(Jmeter)、李珮慈(測試案例撰寫)、黃莉庭(主要測試人員)、王心妤(彙整)
  
  - 李萱: 訂單狀態頁面、顧客點餐頁面(老闆用)、熱門餐點功能
  - 李珮慈: 購物車頁面、測試資料建立、修改單品頁面(支援)、修改套餐頁面(支援)
  - 林怡萱: 忘記密碼功能、編輯菜單頁面、新增單品頁面、新增套餐頁面、修改單品頁面(主要)、修改套餐頁面(主要)
  - 王心妤: 開發流程設計、系統架構設計、API文件維護、後台開發、單元測試撰寫、黑名單頁面、新資訊推播頁面
  - 謝雅芳: UI設計、icon設計、測試資料建立、個人資訊頁面、菜單頁面、餐點製作清單頁面
  - 游傑如: 歷史點菜單頁面、拒絕訂單之顧客推播、單元測試撰寫
  - 黃莉庭: 設定營業時間頁面、系統測試

---

## Github & Trello
  - [github](https://github.com/creek0810/loveat2)
  - [Trello](https://trello.com/b/ls8xqQs8/%E8%BB%9F%E5%B7%A5)

---

## server網址與使用者帳號密碼
- [server](https://loveat2.appspot.com/menu/)
- account
    - admin account
        - user name: admin
        - password: 123456789
    - customer account
        - user name: test8
        - password: 123456789

---

## 提升流程品質或系統品質的措施

- 開發流程
  - 使用github flow進行
  - 使用conventional commit格式撰寫commit message
  - 使用pre commit hook，在每次commit前都會先進行測試，測試成功後才可commit
    - 以husky整合套件，進行hook的配置
    - 使用lint staged，僅對此次修改的檔案進行相對應之測試操作，縮減時間成本
    - 配置
      - javascript file
        - 使用prettier format程式碼
        - eslint測試
      - python file
        - 使用black format程式碼
        - flake8測試(lint)
        - pytest單元測試
  - 使用travis ci
    - 所有branch進行eslint測試
    - 所有branch進行flake8測試
    - 所有branch進行pytest測試
    - merge至master時自動部署至GAE
    - merge至master時自動進行pytest，並將覆蓋率結果上傳至codecov
    - merge至master & commit為"chore(release)"前綴時，使用semantic-release自動release

- lint & formatter
  - python
    - black(formatter)
    - flake8(lint)
  - js
    - prettier(formatter)
    - eslint(lint, 使用airbnb規範)

- 文檔工具
  - swagger

- 參考網址
  - [swagger](https://app.swaggerhub.com/apis-docs/creek0810/loveat2/1.0.0#/)
  - [lint staged](https://github.com/okonet/lint-staged)
  - [husky](https://github.com/typicode/husky)
  - [codecov](https://codecov.io/)
  - [semantic-release](https://github.com/semantic-release/semantic-release)
  - [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/)
  - [black](https://github.com/psf/black)
  - [flake8](https://github.com/PyCQA/flake8)
  - [prettier](https://github.com/prettier/prettier)
  - [eslint](https://github.com/eslint/eslint)

