# 프로젝트 기여 네이밍 컨벤션

이 문서는 `[5조]`가 `[6조]` 프로젝트에 기여할 때 사용하는 이름 규칙(Naming Convention)을 정의합니다.

**문서의 목적:**
1.  **일관성 (Consistency):** 통일된 규칙을 사용해 코드의 가독성을 높입니다.
2.  **명확성 (Clarity):** 이름만 보고도 의도를 파악할 수 있게 합니다.
3.  **충돌 방지 (Conflict Prevention):** 작업 단위와 파일명이 겹치지 않도록 합니다.
4.  **원활한 협업 (Collaboration):** 상대 조가 우리의 기여 내용을 쉽게 이해하고 리뷰할 수 있도록 돕습니다.

-----

## 1. 브랜치 (Branch)

브랜치는 기능 개발, 버그 수정 등 하나의 작업 단위를 나타냅니다. 특히 다른 조와 협업 시, **누가(우리 조가) 무엇을 했는지** 명확히 구분하는 것이 가장 중요합니다.

### 기본 형식

`[type]-[description]`

* **`[type]`:** 작업의 종류를 나타냅니다. (소문자)
    * `feat`: 새로운 기능 추가
    * `fix`: 버그 수정
    * `docs`: 문서 수정 (README, 기여 방법 등)
    * `refactor`: 코드 리팩토링 (기능 변경 없이 코드 구조만 개선)
    * `style`: 코드 스타일 수정 (포맷팅, 세미콜론 추가/삭제 등)
* **`[description]`:** 작업 내용에 대한 간결한 설명.
    * (예: `add_login_page`, `fix_header.css`)

### 좋은 예시

* `feat-add_login_page` (A팀이 로그인 페이지 기능을 추가)
* `fix-user_auth_bug` (A팀이 사용자 인증 버그를 수정)
* `docs-update_readme` (A팀이 README 문서를 수정)

### 나쁜 예시

* `login` (누가, 무슨 작업인지 알 수 없음)
* `feat/로그인페이지` (type과 decs 사이에 `/` 사용)

---

## 2. 폴더 (Directory)

폴더는 관련된 파일들을 그룹화합니다. 이름은 **소문자** 사용을 원칙으로 합니다.

**중요 원칙:**
**`[6조]`의 기존 폴더 규칙을 최우선으로 따릅니다.** 만약 상대 조의 규칙이 명확하지 않을 경우, 아래의 우리 규칙을 적용합니다.

### 기본 형식

* **`kebab-case`** (소문자 + 하이픈)을 사용합니다.
* 일반적으로 여러 파일이 담기므로 **복수형 명사**를 권장합니다.
    * (예: `components`, `utils`, `assets`, `api-services`)

### 좋은 예시

* `components`
* `user-profile`
* `common-utils`
* `assets`

### 나쁜 예시

* `UserProfile` (대문자 사용)
* `util` (너무 모호함)

---

## 3. 파일 (File)

파일 이름은 그 파일의 역할과 내용을 명확히 설명해야 합니다.

**중요 원칙:**
**폴더와 마찬가지로 `[6조]`의 기존 파일 규칙을 최우선으로 따릅니다.**

### 기본 형식

* **일반 파일 (JS/TS 로직, CSS, 이미지 등):**
    * **`kebab-case`** (소문자 + 하이픈)을 사용합니다.
    * (예: `api-client.js`, `auth-service.ts`, `main-layout.css`)
* **컴포넌트 파일 (React, Vue 등):**
    * **`PascalCase`** (대문자로 시작하는 단어 조합)를 사용합니다.
    * (예: `LoginButton.jsx`, `UserProfile.vue`, `CommonModal.tsx`)

### 좋은 예시

* `auth-service.js` (기능/서비스 로직)
* `user-api.ts` (API 관련 로직)
* `LoginButton.jsx` (React 컴포넌트)
* `MyPage.vue` (Vue 컴포넌트)
* `icon-check.svg` (이미지/에셋)

### 나쁜 예시

* `test.js` (무엇을 하는 파일인지 불명확)
* `user controller.js` (공백 사용)
* `login_button.jsx` (컴포넌트임에도 `snake_case` 사용)
* `auth.service.js` (점 `.` 을 구분자로 사용)

---

## 4. 커밋 메시지 (Commit Message)

커밋 메시지는 '작업 이력' 그 자체입니다. 명확한 규칙을 따르면 나중에 변경 사항을 추적하거나 릴리즈 노트를 작성할 때 매우 유용합니다.

### 기본 형식 (Conventional Commits)

`[Type(scope)]:[Subject]`

`[Body]`

**1. `Type` (필수):** 커밋의 종류를 나타냅니다.
* `Feat`: 새로운 기능 추가
* `Fix`: 버그 수정
* `Docs`: 문서 수정
* `Style`: 코드 스타일 변경 (포맷팅, 세미콜론 등)
* `Refactor`: 코드 리팩토링

**2. `scope` (선택):** 커밋이 영향을 미치는 범위 (예: `login`, `auth`, `header`)

**3. `Subject` (필수):** 작업 내용 요약
* **첫 글자는 대문자**로 작성합니다.
* "~을 수정함", "~했음" (과거형)이 아닌 **"수정", "추가" (명령문)**로 작성합니다.
* 문장 끝에 마침표(`.`)를 찍지 않습니다.
* 50자 이내로 간결하게 작성합니다.

**4. `Body` (선택):** `Subject`로 설명이 부족할 때, **"무엇을, 왜"** 변경했는지 상세히 작성합니다.

### 좋은 예시

* `Feat: 로그인 페이지 UI 및 기본 기능 추가`
* `Fix(auth): API 요청 시 인증 토큰 누락 문제 수정`
* `Docs: 네이밍 컨벤션 가이드 문서 추가`
* `Style: 전체 파일 ESLint 규칙에 맞게 포맷팅`
* `Refactor(user): getUserInfo 함수 비동기 로직 개선`
* `Feat(header): 헤더 컴포넌트에 알림 아이콘 추가`

    - 사용자가 새로운 알림을 확인할 수 있도록 우측 상단에 아이콘 표시
    - API 연동은 추후 작업 예정

    Closes #42

### 나쁜 예시

* `버그 수정` (Type, Subject 규칙 위반 / 내용 불명확)
* `feat: login page added.` (Subject 첫 글자 소문자, 마침표)
* `고쳤음` (의미 없음)
